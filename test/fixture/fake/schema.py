# ruff: noqa: PGH003
# type: ignore

"""A mock dataset schema and data generator of below structure.

[
    {
        "scalar": "{row_id}",
        "struct": {
            "struct": "struct_struct_scalar_{row_id}",
            "sequence": [
                {
                    "scalar":
                        "struct_sequence_element_struct_scalar_{row_id}_{element_id}",
                },
                ...
            ],
        },
    },
    ...
]
"""

from collections.abc import Mapping, Sequence
from typing import Any, Final

from open_targets.adapter.data_view import DataView
from open_targets.data.metadata.model import OpenTargetsDatasetFieldType
from open_targets.data.schema_base import Dataset, ScalarField, SequenceField, StructField

SCALAR_TYPE_FIELD_NAME: Final[str] = "scalar"
STRUCT_TYPE_FIELD_NAME: Final[str] = "struct"
SEQUENCE_TYPE_FIELD_NAME: Final[str] = "sequence"


class DatasetFake(Dataset):
    f_scalar: Final[type["FieldFakeScalar"]]
    f_struct: Final[type["FieldFakeStruct"]]

    @classmethod
    def get_row(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeScalar.get_value(row_id=row_id),
            cls.f_struct.name: FieldFakeStruct.get_value(row_id=row_id),
        }

    @classmethod
    def get_field_mapped_row(cls, *, row_id: int) -> DataView:
        return {
            cls.f_scalar: FieldFakeScalar.get_value(row_id=row_id),
            cls.f_struct: FieldFakeStruct.get_field_mapped_value(row_id=row_id),
        }


class FieldFakeScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int) -> str:
        return f"{row_id}"


class FieldFakeStruct(StructField):
    f_struct: Final[type["FieldFakeStructStruct"]]
    f_sequence: Final[type["FieldFakeStructSequence"]]

    @classmethod
    def get_value(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_struct.name: FieldFakeStructStruct.get_value(row_id=row_id),
            cls.f_sequence.name: FieldFakeStructSequence.get_value(row_id=row_id, num_elements=2),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int) -> DataView:
        return {
            cls.f_struct: FieldFakeStructStruct.get_field_mapped_value(row_id=row_id),
            cls.f_sequence: FieldFakeStructSequence.get_field_mapped_value(row_id=row_id, num_elements=2),
        }


class FieldFakeStructStruct(StructField):
    f_scalar: Final[type["FieldFakeStructStructScalar"]]

    @classmethod
    def get_value(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeStructStructScalar.get_value(row_id=row_id),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int) -> DataView:
        return {
            cls.f_scalar: FieldFakeStructStructScalar.get_value(row_id=row_id),
        }


class FieldFakeStructSequence(SequenceField):
    @classmethod
    def get_value(cls, *, row_id: int, num_elements: int) -> Sequence[Mapping[str, Any]]:
        return [FieldFakeStructSequenceElement.get_value(row_id=row_id, element_id=i) for i in range(num_elements)]

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int, num_elements: int) -> Sequence[DataView]:
        return [
            FieldFakeStructSequenceElement.get_field_mapped_value(row_id=row_id, element_id=i)
            for i in range(num_elements)
        ]


class FieldFakeStructStructScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int) -> str:
        return f"struct_struct_scalar_{row_id}"


class FieldFakeStructSequenceElement(StructField):
    f_scalar: Final[type["FieldFakeStructSequenceElementScalar"]]

    @classmethod
    def get_value(cls, *, row_id: int, element_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeStructSequenceElementScalar.get_value(row_id=row_id, element_id=element_id),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int, element_id: int) -> DataView:
        return {
            cls.f_scalar: FieldFakeStructSequenceElementScalar.get_value(row_id=row_id, element_id=element_id),
        }


class FieldFakeStructSequenceElementScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int, element_id: int) -> str:
        return f"struct_sequence_element_struct_scalar_{row_id}_{element_id}"


DatasetFake.id = "fake_dataset"
DatasetFake.fields = [
    FieldFakeScalar,
    FieldFakeStruct,
]
DatasetFake.f_scalar = FieldFakeScalar
DatasetFake.f_struct = FieldFakeStruct

FieldFakeScalar.dataset = DatasetFake
FieldFakeScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeScalar.path = [DatasetFake, FieldFakeScalar]

FieldFakeStruct.dataset = DatasetFake
FieldFakeStruct.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeStruct.name = STRUCT_TYPE_FIELD_NAME
FieldFakeStruct.path = [DatasetFake, FieldFakeStruct]
FieldFakeStruct.fields = [FieldFakeStructStruct, FieldFakeStructSequence]
FieldFakeStruct.f_struct = FieldFakeStructStruct
FieldFakeStruct.f_sequence = FieldFakeStructSequence

FieldFakeStructStruct.dataset = DatasetFake
FieldFakeStructStruct.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeStructStruct.name = STRUCT_TYPE_FIELD_NAME
FieldFakeStructStruct.path = [DatasetFake, FieldFakeStruct, FieldFakeStructStruct]
FieldFakeStructStruct.fields = [FieldFakeStructStructScalar]
FieldFakeStructStruct.f_scalar = FieldFakeStructStructScalar

FieldFakeStructSequence.dataset = DatasetFake
FieldFakeStructSequence.data_type = OpenTargetsDatasetFieldType.ARRAY
FieldFakeStructSequence.name = SEQUENCE_TYPE_FIELD_NAME
FieldFakeStructSequence.path = [DatasetFake, FieldFakeStruct, FieldFakeStructSequence]
FieldFakeStructSequence.element = FieldFakeStructSequenceElement

FieldFakeStructStructScalar.dataset = DatasetFake
FieldFakeStructStructScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeStructStructScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeStructStructScalar.path = [DatasetFake, FieldFakeStruct, FieldFakeStructStruct, FieldFakeStructStructScalar]

FieldFakeStructSequenceElement.dataset = DatasetFake
FieldFakeStructSequenceElement.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeStructSequenceElement.name = "element"
FieldFakeStructSequenceElement.path = [
    DatasetFake,
    FieldFakeStruct,
    FieldFakeStructSequence,
    FieldFakeStructSequenceElement,
]
FieldFakeStructSequenceElement.fields = [FieldFakeStructSequenceElementScalar]
FieldFakeStructSequenceElement.f_scalar = FieldFakeStructSequenceElementScalar

FieldFakeStructSequenceElementScalar.dataset = DatasetFake
FieldFakeStructSequenceElementScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeStructSequenceElementScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeStructSequenceElementScalar.path = [
    DatasetFake,
    FieldFakeStruct,
    FieldFakeStructSequence,
    FieldFakeStructSequenceElement,
    FieldFakeStructSequenceElementScalar,
]
