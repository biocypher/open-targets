# pyright: reportUnknownMemberType=false

"""Implementation of the generation context protocol."""

from collections.abc import Iterable, Sequence
from os import PathLike
from pathlib import Path
from typing import Any, Final, cast, overload

import duckdb

from open_targets.adapter.data_wrapper import ConvertedType, DataWrapper, SequencePresentingDataWrapper
from open_targets.adapter.generation_definition import GenerationDefinition
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import FlattenedScanOperation, RowScanOperation, ScanOperation
from open_targets.data.schema_base import Dataset, Field

TOP_FIELD_PATH_LENGTH = 2


class GenerationContext:
    """An implementation of the generation context using duckdb."""

    def __init__(
        self,
        node_definitions: list[GenerationDefinition[NodeInfo]],
        edge_definitions: list[GenerationDefinition[EdgeInfo]],
        datasets_location: str | PathLike[str],
        limit: int | None = None,
    ) -> None:
        """Initialize the generation context.

        Datasets and fields required are automatically computed from the
        provided definitions. Once the context is initialised, the definitions
        are immutable.
        """
        self.node_definitions: Final[list[GenerationDefinition[NodeInfo]]] = node_definitions
        self.edge_definitions: Final[list[GenerationDefinition[EdgeInfo]]] = edge_definitions
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
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        """Get the scan result stream."""
        match scan_operation:
            case RowScanOperation():
                return self._get_row_scan_result_stream(scan_operation.dataset, required_fields)
            case FlattenedScanOperation():
                return self._get_flattened_scan_result_stream(
                    scan_operation.dataset,
                    scan_operation.flattened_field,
                    required_fields,
                )
            case _:
                msg = f"Unsupported scan operation: {scan_operation}"
                raise ValueError(msg)

    def get_generators(self) -> Iterable[Iterable[NodeInfo] | Iterable[EdgeInfo]]:
        """Get the generators of all definitions registered."""
        for definition in self.node_definitions + self.edge_definitions:
            yield definition.generate(self)

    @overload
    def get_generator(self, definition: GenerationDefinition[NodeInfo]) -> Iterable[NodeInfo]: ...

    @overload
    def get_generator(self, definition: GenerationDefinition[EdgeInfo]) -> Iterable[EdgeInfo]: ...

    def get_generator(
        self,
        definition: GenerationDefinition[NodeInfo] | GenerationDefinition[EdgeInfo],
    ) -> Iterable[NodeInfo] | Iterable[EdgeInfo]:
        """Get the generator for a registered definition."""
        if definition not in self.node_definitions + self.edge_definitions:
            msg = f"Definition {definition} was not registered."
            raise ValueError(msg)
        return definition.generate(self)

    def _get_row_scan_result_stream(
        self,
        dataset: type[Dataset],
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        field_index_map, query_result_stream = self._get_query_result(dataset, required_fields)
        return (SequencePresentingDataWrapper(field_index_map, i) for i in query_result_stream)

    def _get_flattened_scan_result_stream(
        self,
        dataset: type[Dataset],
        flattened_field: type[Field],
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        fields_under_flattened_field = [
            field
            for field in required_fields
            if (flattened_field in field.path) and (len(field.path) > len(flattened_field.path))
        ]
        upper_fields = [field for field in required_fields if field not in fields_under_flattened_field]
        field_index_map = {field: index for index, field in enumerate(upper_fields + fields_under_flattened_field)}
        flattened_field_index = field_index_map[flattened_field]
        flattened_field_path_length = len(flattened_field.path)

        for data in self._get_row_scan_result_stream(dataset, upper_fields):
            upper_data = [self._get_value_from_field_path(data, field.path) for field in upper_fields]
            sequence_data = cast(Sequence[DataWrapper], upper_data[flattened_field_index])
            for item in sequence_data:
                lower_data = [
                    self._get_value_from_field_path(item, field.path[flattened_field_path_length:])
                    for field in fields_under_flattened_field
                ]
                yield SequencePresentingDataWrapper(field_index_map, upper_data + lower_data)

    def _get_value_from_field_path(self, data: DataWrapper, field_path: Sequence[type[Field]]) -> ConvertedType:
        value = data[field_path[1]]
        for field in field_path[2:]:
            value = cast(DataWrapper, value)[field]
        return value

    def _get_query_result(
        self,
        dataset: type[Dataset],
        required_fields: Iterable[type[Field]],
    ) -> tuple[dict[type[Field], int], Iterable[tuple[Any]]]:
        top_fields = [field for field in required_fields if len(field.path) == TOP_FIELD_PATH_LENGTH]
        field_index_map = {field: index for index, field in enumerate(top_fields)}
        query = duckdb.read_parquet(str(self.get_dataset_path(dataset))).select(*[field.name for field in top_fields])
        if self.limit is not None:
            query = query.limit(self.limit)
        return field_index_map, self._get_query_result_stream(query)

    def _get_query_result_stream(self, query: duckdb.DuckDBPyRelation) -> Iterable[tuple[Any]]:
        while True:
            item = cast(tuple[Any] | None, query.fetchone())
            if item is None:
                break
            yield item
