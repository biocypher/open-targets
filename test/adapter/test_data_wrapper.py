from collections.abc import Mapping, Sequence
from typing import Any

import pytest

from open_targets.adapter.data_view import (
    ArrayDataView,
    DataViewProtocol,
    MappingBackedDataView,
    SequenceBackedDataView,
)
from open_targets.data.schema_base import Field
from test.fixture.fake.schema import (
    DatasetFake,
    FieldFakeNullElementSequence,
    FieldFakeNullSequence,
    FieldFakeScalar,
    FieldFakeStruct,
    FieldFakeStructSequence,
    FieldFakeStructSequenceElement,
    FieldFakeStructSequenceElementScalar,
    FieldFakeStructStruct,
    FieldFakeStructStructScalar,
)


@pytest.fixture
def dataset_first_row() -> Mapping[str, Any]:
    return DatasetFake.get_row(row_id=0)


@pytest.mark.parametrize(
    "key",
    [FieldFakeScalar, FieldFakeStruct, FieldFakeNullSequence, FieldFakeNullElementSequence],
)
def test_mapping_backed_data_view(dataset_first_row: Mapping[str, Any], key: type[Field]) -> None:
    view = MappingBackedDataView(dataset_first_row, DatasetFake.fields)
    assert_data_view_equals_raw_data(view[key], dataset_first_row[key.name])


@pytest.mark.parametrize(
    "order",
    [
        (FieldFakeScalar, FieldFakeStruct),
        (FieldFakeStruct, FieldFakeScalar),
    ],
)
def test_sequence_backed_data_view(
    dataset_first_row: Mapping[str, Any],
    order: Sequence[type[Field]],
) -> None:
    ordered = tuple(dataset_first_row[field.name] for field in order)
    field_index_dict = {field: index for index, field in enumerate(order)}
    view = SequenceBackedDataView(field_index_dict, ordered, order)

    for field in [FieldFakeScalar, FieldFakeStruct]:
        assert_data_view_equals_raw_data(view[field], dataset_first_row[field.name])


def test_mapping_backed_data_view_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    view = MappingBackedDataView(dataset_first_row, DatasetFake.fields)
    assert set(view.keys()) == {
        FieldFakeScalar,
        FieldFakeStruct,
        FieldFakeNullSequence,
        FieldFakeNullElementSequence,
    }
    nested = view[FieldFakeStruct]
    assert isinstance(nested, MappingBackedDataView)
    assert set(nested.keys()) == {FieldFakeStructStruct, FieldFakeStructSequence}


def test_sequence_backed_data_view_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    field_index_dict: dict[type[Field], int] = {FieldFakeScalar: 0, FieldFakeStruct: 1}
    fields = [FieldFakeScalar, FieldFakeStruct]
    data = tuple(dataset_first_row[field.name] for field in fields)
    view = SequenceBackedDataView(field_index_dict, data, fields)
    assert set(view.keys()) == {FieldFakeScalar, FieldFakeStruct}


@pytest.mark.parametrize(
    ("row", "keys", "expected"),
    [
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeScalar,),
            FieldFakeScalar.get_value(row_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct,),
            FieldFakeStruct.get_value(row_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence),
            FieldFakeStructSequence.get_value(row_id=0, num_elements=2),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructStruct),
            FieldFakeStructStruct.get_value(row_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructStruct, FieldFakeStructStructScalar),
            FieldFakeStructStructScalar.get_value(row_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence, 0),
            FieldFakeStructSequenceElement.get_value(row_id=0, element_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence, 0, FieldFakeStructSequenceElementScalar),
            FieldFakeStructSequenceElementScalar.get_value(row_id=0, element_id=0),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence, 1),
            FieldFakeStructSequenceElement.get_value(row_id=0, element_id=1),
        ),
        (
            DatasetFake.get_row(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence, 1, FieldFakeStructSequenceElementScalar),
            FieldFakeStructSequenceElementScalar.get_value(row_id=0, element_id=1),
        ),
        (
            DatasetFake.get_row_with_null_struct(row_id=0),
            (FieldFakeStruct,),
            FieldFakeStruct.get_null_value(),
        ),
        (
            DatasetFake.get_row_with_null_sequence(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence),
            FieldFakeStructSequence.get_null_value(),
        ),
        (
            DatasetFake.get_row_with_null_element_field(row_id=0),
            (FieldFakeStruct, FieldFakeStructSequence, 0, FieldFakeStructSequenceElementScalar),
            FieldFakeStructSequenceElementScalar.get_null_value(),
        ),
    ],
)
def test_nested_access(row: Mapping[str, Any], keys: tuple[Any], expected: Any) -> None:
    view = MappingBackedDataView(row, DatasetFake.fields)
    value = view
    for key in keys:
        assert isinstance(value, DataViewProtocol)
        value = value[key]

    assert_data_view_equals_raw_data(value, expected)


def test_array_data_view_preserves_null_elements() -> None:
    view = ArrayDataView(FieldFakeStructSequence.get_null_element_value(), [FieldFakeStructSequenceElementScalar])
    null_value = FieldFakeStructSequenceElementScalar.get_null_value()
    assert list(view) == [null_value]
    assert view[0] is null_value
    assert view[:] == [null_value]


def assert_data_view_equals_raw_data(view: Any, data: Any) -> None:
    if isinstance(view, DataViewProtocol):
        assert view.raw_data == data
    else:
        assert view == data
