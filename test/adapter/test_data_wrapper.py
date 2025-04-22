from collections.abc import Mapping, Sequence
from typing import Any

import pytest

from open_targets.adapter.data_view import (
    DataViewProtocol,
    MappingBackedDataView,
    SequenceBackedDataView,
)
from open_targets.data.schema_base import Field
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


@pytest.fixture
def dataset_first_row() -> Mapping[str, Any]:
    return DatasetFake.get_row(row_id=0)


@pytest.mark.parametrize("key", [FieldFakeScalar, FieldFakeStruct, FieldFakeSequence])
def test_mapping_backed_data_view(dataset_first_row: Mapping[str, Any], key: type[Field]) -> None:
    view = MappingBackedDataView(dataset_first_row, DatasetFake.fields)
    assert_data_view_equals_raw_data(view[key], dataset_first_row[key.name])


@pytest.mark.parametrize(
    "order",
    [
        (FieldFakeScalar, FieldFakeStruct, FieldFakeSequence),
        (FieldFakeSequence, FieldFakeScalar, FieldFakeStruct),
        (FieldFakeStruct, FieldFakeSequence, FieldFakeScalar),
    ],
)
def test_sequence_backed_data_view(
    dataset_first_row: Mapping[str, Any],
    order: Sequence[type[Field]],
) -> None:
    ordered = tuple(dataset_first_row[field.name] for field in order)
    field_index_dict = {field: index for index, field in enumerate(order)}
    view = SequenceBackedDataView(field_index_dict, ordered, order)

    for field in [FieldFakeScalar, FieldFakeStruct, FieldFakeSequence]:
        assert_data_view_equals_raw_data(view[field], dataset_first_row[field.name])


def test_mapping_backed_data_view_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    view = MappingBackedDataView(dataset_first_row, DatasetFake.fields)
    assert set(view.keys()) == {FieldFakeScalar, FieldFakeStruct, FieldFakeSequence}
    nested = view[FieldFakeStruct]
    assert isinstance(nested, MappingBackedDataView)
    assert set(nested.keys()) == {FieldFakeStructStruct}


def test_sequence_backed_data_view_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    field_index_dict: dict[type[Field], int] = {FieldFakeScalar: 0, FieldFakeStruct: 1}
    fields = [FieldFakeScalar, FieldFakeStruct]
    data = tuple(dataset_first_row[field.name] for field in fields)
    view = SequenceBackedDataView(field_index_dict, data, fields)
    assert set(view.keys()) == {FieldFakeScalar, FieldFakeStruct}


@pytest.mark.parametrize(
    ("keys", "expected"),
    [
        (
            (FieldFakeScalar,),
            FieldFakeScalar.get_value(row_id=0),
        ),
        (
            (FieldFakeStruct,),
            FieldFakeStruct.get_value(row_id=0),
        ),
        (
            (FieldFakeSequence,),
            FieldFakeSequence.get_value(row_id=0, num_elements=2),
        ),
        (
            (FieldFakeStruct, FieldFakeStructStruct),
            FieldFakeStructStruct.get_value(row_id=0),
        ),
        (
            (FieldFakeStruct, FieldFakeStructStruct, FieldFakeStructStructScalar),
            FieldFakeStructStructScalar.get_value(row_id=0),
        ),
        (
            (FieldFakeSequence, 0),
            FieldFakeSequenceElement.get_value(row_id=0, element_id=0),
        ),
        (
            (FieldFakeSequence, 0, FieldFakeSequenceElementScalar),
            FieldFakeSequenceElementScalar.get_value(row_id=0, element_id=0),
        ),
        (
            (FieldFakeSequence, 1),
            FieldFakeSequenceElement.get_value(row_id=0, element_id=1),
        ),
        (
            (FieldFakeSequence, 1, FieldFakeSequenceElementScalar),
            FieldFakeSequenceElementScalar.get_value(row_id=0, element_id=1),
        ),
    ],
)
def test_nested_access(dataset_first_row: Mapping[str, Any], keys: tuple[Any], expected: Any) -> None:
    view = MappingBackedDataView(dataset_first_row, DatasetFake.fields)
    value = view
    for key in keys:
        assert isinstance(value, DataViewProtocol)
        value = value[key]

    assert_data_view_equals_raw_data(value, expected)


def assert_data_view_equals_raw_data(view: Any, data: Any) -> None:
    if isinstance(view, DataViewProtocol):
        assert view.raw_data == data
    else:
        assert view == data
