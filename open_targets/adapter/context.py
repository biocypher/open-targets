# pyright: reportUnknownMemberType=false

"""Implementation of the acquisition context protocol."""

from collections.abc import Iterable, Mapping, Sequence
from functools import reduce
from os import PathLike
from typing import Any, Final, cast, overload

from duckdb import (
    ColumnExpression,
    ConstantExpression,
    DuckDBPyConnection,
    DuckDBPyRelation,
    Expression,
    connect,
)

from open_targets.adapter.acquisition_definition import AcquisitionDefinition
from open_targets.adapter.data_view import DataView, DataViewProtocol, SequenceBackedDataView
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation, RowScanOperation, ScanOperation
from open_targets.adapter.scan_operation_predicate import (
    AndExpression,
    EqualityExpression,
    NotExpression,
    OrExpression,
    ScanOperationPredicateExpression,
)
from open_targets.data.location import build_dataset_path, resolve_datasets_location
from open_targets.data.metadata.model import OpenTargetsDatasetFieldType
from open_targets.data.schema_base import Dataset, Field, SequenceField

TOP_FIELD_PATH_INDEX = 1
TOP_FIELD_PATH_LENGTH = TOP_FIELD_PATH_INDEX + 1


def _should_drop_exploded_element(
    scan_operation: ExplodingScanOperation,
    item: DataView | None,
) -> bool:
    """Return whether an exploded element should be dropped."""
    drop = scan_operation.drop_null_elements
    if drop is False:
        return False
    if item is None:
        return True
    if drop is True:
        return False
    return any(
        _get_exploded_field_value(cast("DataViewProtocol", item), field, scan_operation.exploded_field) is None
        for field in drop
    )


def _get_exploded_field_value(
    item: DataViewProtocol,
    field: type[Field],
    exploded_field: type[SequenceField],
) -> Any:
    """Resolve a nested field relative to the exploded element."""
    data: Any = item.raw_data
    path = field.path[len(exploded_field.path) + 1 :]
    for nested_field in path:
        if data is None:
            return None
        if isinstance(data, Mapping):
            data = cast("Mapping[str, Any]", data)[cast("type[Field]", nested_field).name]
        else:
            msg = f"Field {field.__name__} is not a mapping field path"
            raise TypeError(msg)
    return data


class AcquisitionContext:
    """An implementation of the acquisition context using duckdb."""

    def __init__(
        self,
        *,
        node_definitions: list[AcquisitionDefinition[NodeInfo]],
        edge_definitions: list[AcquisitionDefinition[EdgeInfo]],
        datasets_location: str | PathLike[str],
        limit: int | None = None,
    ) -> None:
        """Initialize the acquisition context.

        Datasets and fields required are automatically computed from the
        provided definitions. Once the context is initialised, the definitions
        are immutable.

        Args:
            node_definitions (list[AcquisitionDefinition[NodeInfo]]): The
                definitions of the nodes to acquire.
            edge_definitions (list[AcquisitionDefinition[EdgeInfo]]): The
                definitions of the edges to acquire.
            datasets_location (str | PathLike[str]): A local directory, a
                ``file://`` URL, or an ``s3://`` repository root.
            limit (int | None): The maximum number of rows to retrieve from each
                dataset. If None, all rows are retrieved.

        Returns:
            AcquisitionContext: The handler for an acquisition which could be
            used to stream the acquired data using the provided acquisition
            definitions.
        """
        self.node_definitions: Final[list[AcquisitionDefinition[NodeInfo]]] = node_definitions
        self.edge_definitions: Final[list[AcquisitionDefinition[EdgeInfo]]] = edge_definitions
        all_datasets_required: frozenset[type[Dataset]] = frozenset(
            dataset
            for definition in node_definitions + edge_definitions
            for dataset in definition.get_required_datasets()
        )
        self.datasets: Final[frozenset[type[Dataset]]] = all_datasets_required
        is_remote, datasets_location_base = resolve_datasets_location(datasets_location)
        self.is_remote: Final[bool] = is_remote
        self.datasets_location: Final[str] = datasets_location_base
        self.limit: Final[int | None] = limit
        self._connection: Final[DuckDBPyConnection] = connect()
        self._remote_connection_configured: bool = False

    def get_dataset_path(self, dataset: type[Dataset]) -> str:
        """Get the parquet glob path of the dataset."""
        return build_dataset_path(self.datasets_location, dataset, remote=self.is_remote)

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        requested_fields: Sequence[type[Field]],
    ) -> Iterable[DataView]:
        """Get the scan result stream."""
        match scan_operation:
            case RowScanOperation():
                return self._get_row_scan_result_stream(scan_operation, requested_fields)
            case ExplodingScanOperation():
                return self._get_exploded_scan_result_stream(scan_operation, requested_fields)
            case _:
                msg = f"Unsupported scan operation: {scan_operation}"
                raise ValueError(msg)

    def get_acquisition_generators(self) -> Iterable[Iterable[NodeInfo] | Iterable[EdgeInfo]]:
        """Get the acquisition generators of all definitions registered."""
        for definition in self.node_definitions + self.edge_definitions:
            yield definition.acquire(self)

    @overload
    def get_acquisition_generator(self, definition: AcquisitionDefinition[NodeInfo]) -> Iterable[NodeInfo]: ...

    @overload
    def get_acquisition_generator(self, definition: AcquisitionDefinition[EdgeInfo]) -> Iterable[EdgeInfo]: ...

    def get_acquisition_generator(
        self,
        definition: AcquisitionDefinition[NodeInfo] | AcquisitionDefinition[EdgeInfo],
    ) -> Iterable[NodeInfo] | Iterable[EdgeInfo]:
        """Get the acquisition generator for a registered definition."""
        if definition not in self.node_definitions + self.edge_definitions:
            msg = f"Definition {definition} was not registered."
            raise ValueError(msg)
        return definition.acquire(self)

    def _get_row_scan_result_stream(
        self,
        scan_operation: RowScanOperation,
        requested_fields: Sequence[type[Field]],
    ) -> Iterable[DataView]:
        dataset = scan_operation.dataset
        top_fields, nested_fields = self._compute_field_hierarchy(requested_fields, TOP_FIELD_PATH_INDEX)
        field_index_map = {field: index for index, field in enumerate(top_fields)}
        field_path_map: dict[type[Field], int | Sequence[type[Field]]] = {
            field: cast("Sequence[type[Field]]", field.path[TOP_FIELD_PATH_INDEX:]) for field in nested_fields
        }
        field_path_map.update(field_index_map)
        query_result_stream = self._get_query_result(dataset, scan_operation.predicate, top_fields)
        for data in query_result_stream:
            yield SequenceBackedDataView(field_path_map, data, requested_fields)

    def _get_exploded_scan_result_stream(
        self,
        scan_operation: ExplodingScanOperation,
        requested_fields: Sequence[type[Field]],
    ) -> Iterable[DataView]:
        dataset = scan_operation.dataset
        exploded_field = scan_operation.exploded_field
        required_fields = [exploded_field, *requested_fields]
        top_fields, nested_fields = self._compute_field_hierarchy(required_fields, TOP_FIELD_PATH_INDEX)
        field_index_map = {field: index for index, field in enumerate([*top_fields, exploded_field.element])}
        nested_fields_above_exploded_field = [
            field for field in nested_fields if len(field.path) <= len(exploded_field.path)
        ]
        nested_fields_under_exploded_field = [
            field for field in nested_fields if len(field.path) > len(exploded_field.element.path)
        ]
        field_path_map: dict[type[Field], int | Sequence[type[Field]]] = {}
        field_path_map.update(field_index_map)
        field_path_map.update(
            {
                field: cast("Sequence[type[Field]]", field.path[TOP_FIELD_PATH_INDEX:])
                for field in nested_fields_above_exploded_field
            },
        )
        field_path_map.update(
            {
                field: cast("Sequence[type[Field]]", field.path[len(exploded_field.path) :])
                for field in nested_fields_under_exploded_field
            },
        )

        if exploded_field.element.data_type in (OpenTargetsDatasetFieldType.ARRAY, OpenTargetsDatasetFieldType.STRUCT):

            def exploded_field_element_raw_data_getter(item: Any) -> Any:
                if item is None:
                    return None
                return cast("DataViewProtocol", item).raw_data
        else:

            def exploded_field_element_raw_data_getter(item: Any) -> Any:
                return item

        for data in self._get_query_result(dataset, scan_operation.predicate, top_fields):
            view = SequenceBackedDataView(field_path_map, data, required_fields)
            sequence_data = cast("Sequence[DataView | None] | None", view[exploded_field])
            if sequence_data is None:
                if scan_operation.drop_null_elements is not False:
                    continue
                yield SequenceBackedDataView(
                    field_path_map,
                    [*data, None],
                    requested_fields,
                )
            else:
                for item in sequence_data:
                    raw_data = exploded_field_element_raw_data_getter(item)
                    if _should_drop_exploded_element(scan_operation, item):
                        continue
                    yield SequenceBackedDataView(
                        field_path_map,
                        [*data, raw_data],
                        requested_fields,
                    )

    def _compute_field_hierarchy(
        self,
        fields: Iterable[type[Field]],
        starting_position: int,
    ) -> tuple[list[type[Field]], list[type[Field]]]:
        top_fields = list({cast("type[Field]", field.path[starting_position]) for field in fields})
        nested_fields = [field for field in fields if field not in top_fields]
        return top_fields, nested_fields

    def _get_query_result(
        self,
        dataset: type[Dataset],
        predicate: ScanOperationPredicateExpression | None,
        fields: Iterable[type[Field]],
    ) -> Iterable[tuple[Any]]:
        if self.is_remote:
            self._ensure_remote_connection()
        query = self._connection.read_parquet(self.get_dataset_path(dataset), hive_partitioning=True)

        if predicate is not None:
            query = query.filter(self._build_duckdb_filter_expression(None, predicate))

        query = query.select(*[field.name for field in fields])

        if self.limit is not None:
            query = query.limit(self.limit)

        return self._get_query_result_stream(query)

    def _ensure_remote_connection(self) -> None:
        """Install and configure the DuckDB extension for remote datasets."""
        if self._remote_connection_configured:
            return
        self._connection.execute("INSTALL httpfs")
        self._connection.execute("LOAD httpfs")
        self._connection.execute("SET http_timeout = 30")
        self._connection.execute("SET http_retries = 3")
        self._remote_connection_configured = True

    def _get_query_result_stream(self, query: DuckDBPyRelation) -> Iterable[tuple[Any]]:
        # TODO(<Paul>): Proper logging here
        # https://github.com/biocypher/open-targets/issues/72
        retry = 0
        while True:
            try:
                item = cast("tuple[Any] | None", query.fetchone())
                if item is None:
                    break
                retry = 0
                yield item
            except Exception as e:
                print(f"Error {e}")
                if retry < 5:
                    print(f"Retry {retry}")
                    retry = retry + 1
                    continue
                break

    def _build_duckdb_filter_expression(
        self,
        duckdb_expression: Expression | None,
        expression: ScanOperationPredicateExpression,
    ) -> Expression:
        match expression:
            case EqualityExpression():
                if expression.value is None:
                    return ColumnExpression(expression.field.name).isnull()
                return ColumnExpression(expression.field.name) == ConstantExpression(expression.value)
            case NotExpression():
                return ~self._build_duckdb_filter_expression(duckdb_expression, expression.expression)
            case AndExpression():
                return reduce(
                    lambda a, b: a & b,
                    [self._build_duckdb_filter_expression(duckdb_expression, e) for e in expression.expressions],
                )
            case OrExpression():
                return reduce(
                    lambda a, b: a | b,
                    [self._build_duckdb_filter_expression(duckdb_expression, e) for e in expression.expressions],
                )
            case _:
                msg = f"Unsupported predicate: {expression}"
                raise ValueError(msg)
