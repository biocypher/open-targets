from collections.abc import Mapping, Sequence
from typing import Any

import pytest

from open_targets.adapter.data_wrapper import (
    DataWrapper,
    MappingPresentingDataWrapper,
    SequencePresentingDataWrapper,
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
def test_mapping_presenting_data_wrapper(dataset_first_row: Mapping[str, Any], key: type[Field]) -> None:
    wrapped = MappingPresentingDataWrapper(dataset_first_row, DatasetFake.fields)
    assert_wrapped_data_equals_raw_data(wrapped[key], dataset_first_row[key.name])


@pytest.mark.parametrize(
    "order",
    [
        (FieldFakeScalar, FieldFakeStruct, FieldFakeSequence),
        (FieldFakeSequence, FieldFakeScalar, FieldFakeStruct),
        (FieldFakeStruct, FieldFakeSequence, FieldFakeScalar),
    ],
)
def test_sequence_presenting_data_wrapper(
    dataset_first_row: Mapping[str, Any],
    order: Sequence[type[Field]],
) -> None:
    ordered = tuple(dataset_first_row[field.name] for field in order)
    field_index_dict = {field: index for index, field in enumerate(order)}
    wrapped = SequencePresentingDataWrapper(field_index_dict, ordered, order)

    for field in [FieldFakeScalar, FieldFakeStruct, FieldFakeSequence]:
        assert_wrapped_data_equals_raw_data(wrapped[field], dataset_first_row[field.name])


def test_mapping_presenting_data_wrapper_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    wrapped = MappingPresentingDataWrapper(dataset_first_row, DatasetFake.fields)
    assert set(wrapped.keys()) == {FieldFakeScalar, FieldFakeStruct, FieldFakeSequence}
    nested = wrapped[FieldFakeStruct]
    assert isinstance(nested, MappingPresentingDataWrapper)
    assert set(nested.keys()) == {FieldFakeStructStruct}


def test_sequence_presenting_data_wrapper_get_keys(dataset_first_row: Mapping[str, Any]) -> None:
    field_index_dict: dict[type[Field], int] = {FieldFakeScalar: 0, FieldFakeStruct: 1}
    fields = [FieldFakeScalar, FieldFakeStruct]
    data = tuple(dataset_first_row[field.name] for field in fields)
    wrapped = SequencePresentingDataWrapper(field_index_dict, data, fields)
    assert set(wrapped.keys()) == {FieldFakeScalar, FieldFakeStruct}


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
    wrapped = MappingPresentingDataWrapper(dataset_first_row, DatasetFake.fields)
    value = wrapped
    for key in keys:
        assert isinstance(value, DataWrapper)
        value = value[key]

    assert_wrapped_data_equals_raw_data(value, expected)


def assert_wrapped_data_equals_raw_data(wrapped: Any, data: Any) -> None:
    if isinstance(wrapped, DataWrapper):
        assert wrapped.raw_data == data
    else:
        assert wrapped == data
