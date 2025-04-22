# pyright: reportUnknownMemberType=false

"""Implementation of the acquisition context protocol."""

from collections.abc import Iterable, Sequence
from os import PathLike
from pathlib import Path
from typing import Any, Final, cast, overload

import duckdb

from open_targets.adapter.acquisition_definition import AcquisitionDefinition
from open_targets.adapter.data_view import DataView, DataViewProtocol, DataViewValue, SequenceBackedDataView
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation, RowScanOperation, ScanOperation
from open_targets.data.schema_base import Dataset, Field, SequenceField

TOP_FIELD_PATH_INDEX = 1
TOP_FIELD_PATH_LENGTH = TOP_FIELD_PATH_INDEX + 1


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
            datasets_location (str | PathLike[str]): The location of the
                directory containing the datasets.
            limit (int | None): The maximum number of rows to retrieve from each
                dataset. If None, all rows are retrieved.

        Returns:
            AcquisitionContext: The acquisition context that can be used to
                get generators of definitions to stream the acquired data.
        """
        self.node_definitions: Final[list[AcquisitionDefinition[NodeInfo]]] = node_definitions
        self.edge_definitions: Final[list[AcquisitionDefinition[EdgeInfo]]] = edge_definitions
        all_datasets_required: frozenset[type[Dataset]] = frozenset(
            dataset
            for definition in node_definitions + edge_definitions
            for dataset in definition.get_required_datasets()
        )
        self.datasets: Final[frozenset[type[Dataset]]] = all_datasets_required
        self.datasets_location: Final[str | PathLike[str]] = datasets_location
        self.limit: Final[int | None] = limit

    def get_dataset_path(self, dataset: type[Dataset]) -> Path:
        """Get the path to the dataset."""
        return Path(self.datasets_location) / dataset.id / "**" / "*.parquet"

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        requested_fields: Iterable[type[Field]],
    ) -> Iterable[DataView]:
        """Get the scan result stream."""
        match scan_operation:
            case RowScanOperation():
                return self._get_row_scan_result_stream(scan_operation.dataset, requested_fields)
            case ExplodingScanOperation():
                return self._get_exploded_scan_result_stream(
                    scan_operation.dataset,
                    scan_operation.exploded_field,
                    requested_fields,
                )
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
        dataset: type[Dataset],
        requested_fields: Iterable[type[Field]],
    ) -> Iterable[DataView]:
        top_fields, nested_fields = self._compute_field_hierarchy(requested_fields, TOP_FIELD_PATH_INDEX)
        field_index_map = {field: index for index, field in enumerate(top_fields + nested_fields)}
        query_result_stream = self._get_query_result(dataset, top_fields)
        for data in query_result_stream:
            view = SequenceBackedDataView(field_index_map, data, top_fields)
            nested_data = tuple(
                self._deep_get_item(view, cast("Sequence[type[Field]]", field.path[TOP_FIELD_PATH_INDEX:]))
                for field in nested_fields
            )
            yield SequenceBackedDataView(field_index_map, data + nested_data, requested_fields)

    def _get_exploded_scan_result_stream(
        self,
        dataset: type[Dataset],
        exploded_field: type[SequenceField],
        requested_fields: Iterable[type[Field]],
    ) -> Iterable[DataView]:
        fields_under_exploded_field = [
            field
            for field in requested_fields
            if (exploded_field in field.path) and (len(field.path) > len(exploded_field.path))
        ]
        fields_above_exploded_field = [field for field in requested_fields if field not in fields_under_exploded_field]
        field_index_map = {
            field: index for index, field in enumerate(fields_above_exploded_field + fields_under_exploded_field)
        }
        exploded_field_path_length = len(exploded_field.path)

        for view in self._get_row_scan_result_stream(dataset, [exploded_field, *fields_above_exploded_field]):
            sequence_data = cast("Sequence[DataView]", view[exploded_field])
            upper_data = [
                self._deep_get_item(view, cast("Sequence[type[Field]]", field.path[TOP_FIELD_PATH_INDEX:]))
                for field in fields_above_exploded_field
            ]
            for item in sequence_data:
                lower_data = [
                    self._deep_get_item(
                        item,
                        cast("Sequence[type[Field]]", field.path[exploded_field_path_length + 1 :]),
                    )
                    for field in fields_under_exploded_field
                ]
                yield SequenceBackedDataView(field_index_map, upper_data + lower_data, requested_fields)

    def _compute_field_hierarchy(
        self,
        fields: Iterable[type[Field]],
        starting_position: int,
    ) -> tuple[list[type[Field]], list[type[Field]]]:
        top_fields = list({cast("type[Field]", field.path[starting_position]) for field in fields})
        nested_fields = [field for field in fields if field not in top_fields]
        return top_fields, nested_fields

    def _deep_get_item(
        self,
        data: DataViewValue,
        path: Sequence[type[Field]],
    ) -> Any:
        value = data
        for field in path:
            value = cast("DataView", value)[field]
        if isinstance(value, DataViewProtocol):
            return value.raw_data
        return value

    def _get_query_result(
        self,
        dataset: type[Dataset],
        fields: Iterable[type[Field]],
    ) -> Iterable[tuple[Any]]:
        query = duckdb.read_parquet(str(self.get_dataset_path(dataset))).select(*[field.name for field in fields])
        if self.limit is not None:
            query = query.limit(self.limit)
        return self._get_query_result_stream(query)

    def _get_query_result_stream(self, query: duckdb.DuckDBPyRelation) -> Iterable[tuple[Any]]:
        while True:
            item = cast("tuple[Any] | None", query.fetchone())
            if item is None:
                break
            yield item
