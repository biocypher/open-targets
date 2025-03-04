# pyright: reportUnknownMemberType=false

from collections.abc import Iterable
from os import PathLike
from pathlib import Path
from typing import Any, Final, TypeAlias, cast, overload

import duckdb

from open_targets.adapter.data_wrapper import ConvertedType, DataWrapper, SequencePresentingDataWrapper
from open_targets.adapter.generation_context import GenerationContext
from open_targets.adapter.generation_definition import GenerationDefinition
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import FlatteningScanOperation, RowScanOperation, ScanOperation
from open_targets.data.schema_base import Dataset, Field

TGenericGenerationDefinition: TypeAlias = GenerationDefinition[NodeInfo] | GenerationDefinition[EdgeInfo]


TOP_FIELD_PATH_LENGTH = 2


class _GenerationContextImpl(GenerationContext):
    def __init__(
        self,
        node_definitions: list[GenerationDefinition[NodeInfo]],
        edge_definitions: list[GenerationDefinition[EdgeInfo]],
        datasets_location: str | PathLike[str],
    ) -> None:
        all_datasets_required: frozenset[type[Dataset]] = frozenset(
            dataset
            for definition in node_definitions + edge_definitions
            for dataset in definition.get_required_datasets()
        )
        self._datasets: Final[frozenset[type[Dataset]]] = all_datasets_required
        self.datasets_location: Final[str | PathLike[str]] = datasets_location

    @property
    def datasets(self) -> frozenset[type[Dataset]]:
        return self._datasets

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        match scan_operation:
            case RowScanOperation():
                return self._get_row_scan_result_stream(scan_operation.dataset, required_fields)
            case FlatteningScanOperation():
                return self._get_flattening_scan_result_stream(
                    scan_operation.dataset,
                    scan_operation.flattened_field,
                    required_fields,
                )
            case _:
                msg = f"Unsupported scan operation: {scan_operation}"
                raise ValueError(msg)

    def _get_row_scan_result_stream(
        self,
        dataset: type[Dataset],
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        field_index_map, query_result_stream = self._get_query_result(dataset, required_fields)
        return (SequencePresentingDataWrapper(field_index_map, i) for i in query_result_stream)

    def _get_flattening_scan_result_stream(
        self,
        dataset: type[Dataset],
        flattened_field: type[Field],
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        # fields_sorted_by_depth = sorted(required_fields, key=lambda field: len(field.path))
        # placeholders: list[Any] = [None] * len(fields_sorted_by_depth)
        # for row in self._get_row_scan_result_stream(dataset, required_fields):
        #     for field in flattened_field.path:
        #         if isinstance(field, SequenceField):
        #             pass
        raise NotImplementedError

    def _recursive_expand(
        self,
        data: ConvertedType,
        current_level: type[Field],
        flattened_field: type[Field],
        sorted_required_fields: list[type[Field]],
        placeholders: list[Any],
    ) -> Iterable[DataWrapper]:
        # if isinstance(current_level, SequenceField) and len(current_level.path) <= len(flattened_field.path):
        #     for item in data:
        #         yield from self._recursive_expand(item, current_level.element_type, flattened_field)
        # else:
        #     yield data
        raise NotImplementedError

    def _get_query_result(
        self,
        dataset: type[Dataset],
        required_fields: Iterable[type[Field]],
    ) -> tuple[dict[type[Field], int], Iterable[tuple[Any]]]:
        top_fields = [field for field in required_fields if len(field.path) == TOP_FIELD_PATH_LENGTH]
        field_index_map = {field: index for index, field in enumerate(top_fields)}
        fields = ", ".join(f'"{field.name}"' for field in top_fields)
        parquet_partitions_path = Path(self.datasets_location) / dataset.id / "*.parquet"
        query = f"SELECT {fields} FROM read_parquet('{parquet_partitions_path}') LIMIT 100"  # noqa: S608
        return field_index_map, self._get_query_result_stream(query)

    def _get_query_result_stream(self, query: str) -> Iterable[tuple[Any]]:
        query_result = duckdb.sql(query)
        while True:
            item = cast(tuple[Any] | None, query_result.fetchone())
            if item is None:
                break
            yield item


class Adapter:
    def __init__(
        self,
        node_definitions: Iterable[GenerationDefinition[NodeInfo]],
        edge_definitions: Iterable[GenerationDefinition[EdgeInfo]],
        static_properties: Iterable[tuple[str, str]],
        datasets_location: str | PathLike[str],
    ):
        self.node_definitions: Final[list[GenerationDefinition[NodeInfo]]] = list(node_definitions)
        self.edge_definitions: Final[list[GenerationDefinition[EdgeInfo]]] = list(edge_definitions)
        self.static_properties: Final[list[tuple[str, str]]] = list(static_properties)
        self.datasets_location: Final[str | PathLike[str]] = datasets_location
        self.context: Final[GenerationContext] = _GenerationContextImpl(
            self.node_definitions,
            self.edge_definitions,
            self.datasets_location,
        )

    def get_generators(self) -> Iterable[Iterable[NodeInfo] | Iterable[EdgeInfo]]:
        for definition in self.node_definitions + self.edge_definitions:
            yield definition.generate(self.context)

    @overload
    def get_generator(self, definition: GenerationDefinition[NodeInfo]) -> Iterable[NodeInfo]: ...

    @overload
    def get_generator(self, definition: GenerationDefinition[EdgeInfo]) -> Iterable[EdgeInfo]: ...

    def get_generator(self, definition: TGenericGenerationDefinition) -> Iterable[NodeInfo] | Iterable[EdgeInfo]:
        if definition not in self.node_definitions + self.edge_definitions:
            msg = f"Definition {definition} was not registered."
            raise ValueError(msg)
        return definition.generate(self.context)
