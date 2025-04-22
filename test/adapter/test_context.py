from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import pytest

from open_targets.adapter.context import AcquisitionContext
from open_targets.adapter.data_view import ArrayDataView, MappingBackedDataView, SequenceBackedDataView
from open_targets.adapter.scan_operation import ExplodingScanOperation, RowScanOperation
from open_targets.data.schema_base import Dataset, Field
from test.fixture.fake.schema import (
    DatasetFake,
    FieldFakeScalar,
    FieldFakeSequence,
    FieldFakeSequenceElement,
    FieldFakeSequenceElementScalar,
    FieldFakeStruct,
    FieldFakeStructStruct,
    FieldFakeStructStructScalar,
)


def mock_get_query_result_field_value(field: type[Field]) -> Any:
    if field is FieldFakeScalar or field is FieldFakeStruct:
        return field.get_value(row_id=0)
    if field is FieldFakeSequence:
        return field.get_value(row_id=0, num_elements=2)
    msg = f"Field {field} is not a top field"
    raise ValueError(msg)


def mock_get_query_result(dataset: type[Dataset], fields: Iterable[type[Field]]) -> Iterable[tuple[Any]]:
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
        ((FieldFakeScalar, FieldFakeStruct, FieldFakeSequence), DatasetFake.get_field_mapped_row(row_id=0)),
        ((FieldFakeSequence, FieldFakeScalar, FieldFakeStruct), DatasetFake.get_field_mapped_row(row_id=0)),
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
        RowScanOperation(DatasetFake),
        requested_fields,
    )
    result = next(iter(stream))
    result = _serialise(result)
    assert result == expected_result


@pytest.mark.parametrize(
    ("requested_fields", "expected_result"),
    [
        (
            (FieldFakeSequenceElement,),
            [
                {
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=0),
                },
                {
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=1),
                },
            ],
        ),
        (
            (FieldFakeSequenceElementScalar,),
            [
                {
                    FieldFakeSequenceElementScalar: FieldFakeSequenceElementScalar.get_value(row_id=0, element_id=0),
                },
                {
                    FieldFakeSequenceElementScalar: FieldFakeSequenceElementScalar.get_value(row_id=0, element_id=1),
                },
            ],
        ),
        (
            (FieldFakeSequence, FieldFakeSequenceElement),
            [
                {
                    FieldFakeSequence: FieldFakeSequence.get_field_mapped_value(row_id=0, num_elements=2),
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=0),
                },
                {
                    FieldFakeSequence: FieldFakeSequence.get_field_mapped_value(row_id=0, num_elements=2),
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=1),
                },
            ],
        ),
        (
            (FieldFakeScalar, FieldFakeSequenceElement),
            [
                {
                    FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=0),
                },
                {
                    FieldFakeScalar: FieldFakeScalar.get_value(row_id=0),
                    FieldFakeSequenceElement: FieldFakeSequenceElement.get_field_mapped_value(row_id=0, element_id=1),
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
        ExplodingScanOperation(DatasetFake, FieldFakeSequence),
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
