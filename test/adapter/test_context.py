import os
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

import duckdb
import pytest

from open_targets.adapter.context import AcquisitionContext
from open_targets.adapter.data_view import ArrayDataView, MappingBackedDataView, SequenceBackedDataView
from open_targets.adapter.scan_operation import ExplodingScanOperation, RowScanOperation
from open_targets.adapter.scan_operation_predicate import ScanOperationPredicateExpression
from open_targets.config import DATA_REPOSITORY_URLS_S3
from open_targets.data.schema import DatasetTarget, FieldTargetId
from open_targets.data.schema_base import Dataset, Field
from test.fixture.fake.schema import (
    DatasetFake,
    FieldFakeScalar,
    FieldFakeStruct,
    FieldFakeStructSequence,
    FieldFakeStructSequenceElement,
    FieldFakeStructSequenceElementScalar,
    FieldFakeStructStruct,
    FieldFakeStructStructScalar,
)


def mock_get_query_result_field_value(field: type[Field]) -> Any:
    if field is FieldFakeScalar or field is FieldFakeStruct:
        return field.get_value(row_id=0)
    if field is FieldFakeStructSequence:
        return field.get_value(row_id=0, num_elements=2)
    msg = f"Field {field} is not a top field"
    raise ValueError(msg)


def mock_get_query_result(
    dataset: type[Dataset],
    predicate: ScanOperationPredicateExpression | None,
    fields: Iterable[type[Field]],
) -> Iterable[tuple[Any]]:
    return [tuple(mock_get_query_result_field_value(field) for field in fields)]


@pytest.fixture
def context(requested_fields: Sequence[type[Field]]) -> AcquisitionContext:
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location="",
    )
    context._get_query_result = mock_get_query_result
    return context


@pytest.mark.parametrize(
    ("requested_fields", "expected_result"),
    [
        (
            (FieldFakeScalar, FieldFakeStruct, FieldFakeStructSequence),
            {
                FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                FieldFakeStruct: FieldFakeStruct.get_field_mapped_value(row_id=0),
                FieldFakeStructSequence: FieldFakeStructSequence.get_field_mapped_value(row_id=0, num_elements=2),
            },
        ),
        (
            (FieldFakeStructSequence, FieldFakeScalar, FieldFakeStruct),
            {
                FieldFakeStructSequence: FieldFakeStructSequence.get_field_mapped_value(row_id=0, num_elements=2),
                FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                FieldFakeStruct: FieldFakeStruct.get_field_mapped_value(row_id=0),
            },
        ),
        ((FieldFakeScalar,), {FieldFakeScalar: FieldFakeScalar.get_value(row_id=0)}),
        ((FieldFakeStructStruct,), {FieldFakeStructStruct: FieldFakeStructStruct.get_field_mapped_value(row_id=0)}),
        (
            (FieldFakeStructStructScalar,),
            {FieldFakeStructStructScalar: FieldFakeStructStructScalar.get_value(row_id=0)},
        ),
        (
            (FieldFakeStructStructScalar, FieldFakeStructStruct),
            {
                FieldFakeStructStructScalar: FieldFakeStructStructScalar.get_value(row_id=0),
                FieldFakeStructStruct: FieldFakeStructStruct.get_field_mapped_value(row_id=0),
            },
        ),
    ],
)
def test_get_scan_result_stream_row_scan_operation(
    context: AcquisitionContext,
    requested_fields: Sequence[type[Field]],
    expected_result: Sequence[Any],
) -> None:
    stream = context.get_scan_result_stream(
        RowScanOperation(dataset=DatasetFake),
        requested_fields,
    )
    result = next(iter(stream))
    result = _serialise(result)
    assert result == expected_result


@pytest.mark.parametrize(
    ("requested_fields", "expected_result"),
    [
        (
            (FieldFakeStructSequenceElement,),
            [
                {
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=0,
                    ),
                },
                {
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=1,
                    ),
                },
            ],
        ),
        (
            (FieldFakeStructSequenceElementScalar,),
            [
                {
                    FieldFakeStructSequenceElementScalar: FieldFakeStructSequenceElementScalar.get_value(
                        row_id=0,
                        element_id=0,
                    ),
                },
                {
                    FieldFakeStructSequenceElementScalar: FieldFakeStructSequenceElementScalar.get_value(
                        row_id=0,
                        element_id=1,
                    ),
                },
            ],
        ),
        (
            (FieldFakeStructSequence, FieldFakeStructSequenceElement),
            [
                {
                    FieldFakeStructSequence: FieldFakeStructSequence.get_field_mapped_value(row_id=0, num_elements=2),
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=0,
                    ),
                },
                {
                    FieldFakeStructSequence: FieldFakeStructSequence.get_field_mapped_value(row_id=0, num_elements=2),
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=1,
                    ),
                },
            ],
        ),
        (
            (FieldFakeScalar, FieldFakeStructSequenceElement),
            [
                {
                    FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=0,
                    ),
                },
                {
                    FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                    FieldFakeStructSequenceElement: FieldFakeStructSequenceElement.get_field_mapped_value(
                        row_id=0,
                        element_id=1,
                    ),
                },
            ],
        ),
    ],
)
def test_get_scan_result_stream_exploding_scan_operation(
    context: AcquisitionContext,
    requested_fields: Sequence[type[Field]],
    expected_result: Sequence[Any],
) -> None:
    stream = context.get_scan_result_stream(
        ExplodingScanOperation(dataset=DatasetFake, exploded_field=FieldFakeStructSequence),
        requested_fields,
    )
    result = list(stream)
    result = [_serialise(i) for i in result]
    assert result == expected_result


def _serialise(
    value: Any,
) -> Sequence[Any] | Mapping[type[Field], Any]:
    if isinstance(value, ArrayDataView):
        return [_serialise(i) for i in value]
    if isinstance(value, SequenceBackedDataView):
        return {i: _serialise(v) for i, v in value.items()}
    if isinstance(value, MappingBackedDataView):
        return {i: _serialise(v) for i, v in value.items()}
    return value


def test_get_dataset_path_local() -> None:
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location="datasets",
    )
    assert context.is_remote is False
    assert context.get_dataset_path(DatasetTarget) == "datasets/target/**/*.parquet"


def test_get_dataset_path_local_file_url(tmp_path: Path) -> None:
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location=f"file://{tmp_path}",
    )
    assert context.is_remote is False
    assert context.get_dataset_path(DatasetTarget) == str(tmp_path / "target" / "**" / "*.parquet")


def test_get_dataset_path_remote_s3() -> None:
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location=DATA_REPOSITORY_URLS_S3,
    )
    assert context.is_remote is True
    assert context.get_dataset_path(DatasetTarget) == f"{DATA_REPOSITORY_URLS_S3}target/**/*.parquet"


def test_get_scan_result_stream_from_local_path(tmp_path: Path) -> None:
    dataset_dir = tmp_path / DatasetTarget.id
    dataset_dir.mkdir()
    connection = duckdb.connect()
    connection.sql("SELECT * FROM (VALUES ('ENSG1'), ('ENSG2')) AS t(id)").write_parquet(
        str(dataset_dir / "data.parquet"),
    )
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location=tmp_path,
    )
    stream = context.get_scan_result_stream(RowScanOperation(dataset=DatasetTarget), [FieldTargetId])
    assert [row[FieldTargetId] for row in stream] == ["ENSG1", "ENSG2"]


@pytest.mark.skipif(
    not os.environ.get("OPEN_TARGETS_S3_INTEGRATION"),
    reason="Set OPEN_TARGETS_S3_INTEGRATION=1 to run S3 integration tests.",
)
def test_get_scan_result_stream_from_s3() -> None:
    context = AcquisitionContext(
        node_definitions=[],
        edge_definitions=[],
        datasets_location=DATA_REPOSITORY_URLS_S3,
        limit=3,
    )
    stream = context.get_scan_result_stream(RowScanOperation(dataset=DatasetTarget), [FieldTargetId])
    assert len(list(stream)) == context.limit
