# ruff: noqa: PGH003
# type: ignore

"""A mock dataset schema and data generator of below structure.

[
    {
        "scalar": "{row_id}",
        "struct": {
            "struct": "struct_struct_scalar_{row_id}",
        },
        "sequence": [
            {
                "scalar":
                    "sequence_element_struct_scalar_{row_id}_{element_id}",
            },
            ...
        ],
    },
    ...
]
"""

from collections.abc import Mapping, Sequence
from typing import Any, Final

from open_targets.adapter.data_wrapper import FieldMap
from open_targets.data.metadata.model import OpenTargetsDatasetFieldType
from open_targets.data.schema_base import Dataset, ScalarField, SequenceField, StructField

SCALAR_TYPE_FIELD_NAME: Final[str] = "scalar"
STRUCT_TYPE_FIELD_NAME: Final[str] = "struct"
SEQUENCE_TYPE_FIELD_NAME: Final[str] = "sequence"


class DatasetFake(Dataset):
    f_scalar: Final[type["FieldFakeScalar"]]
    f_struct: Final[type["FieldFakeStruct"]]
    f_sequence: Final[type["FieldFakeSequence"]]

    @classmethod
    def get_row(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeScalar.get_value(row_id=row_id),
            cls.f_struct.name: FieldFakeStruct.get_value(row_id=row_id),
            cls.f_sequence.name: FieldFakeSequence.get_value(row_id=row_id, num_elements=2),
        }

    @classmethod
    def get_field_mapped_row(cls, *, row_id: int) -> FieldMap:
        return {
            cls.f_scalar: FieldFakeScalar.get_value(row_id=row_id),
            cls.f_struct: FieldFakeStruct.get_field_mapped_value(row_id=row_id),
            cls.f_sequence: FieldFakeSequence.get_field_mapped_value(row_id=row_id, num_elements=2),
        }


class FieldFakeScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int) -> str:
        return f"{row_id}"


class FieldFakeStruct(StructField):
    f_struct: Final[type["FieldFakeStructStruct"]]

    @classmethod
    def get_value(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_struct.name: FieldFakeStructStruct.get_value(row_id=row_id),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int) -> FieldMap:
        return {
            cls.f_struct: FieldFakeStructStruct.get_field_mapped_value(row_id=row_id),
        }


class FieldFakeSequence(SequenceField):
    @classmethod
    def get_value(cls, *, row_id: int, num_elements: int) -> Sequence[Mapping[str, Any]]:
        return [FieldFakeSequenceElement.get_value(row_id=row_id, element_id=i) for i in range(num_elements)]

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int, num_elements: int) -> Sequence[FieldMap]:
        return [
            FieldFakeSequenceElement.get_field_mapped_value(row_id=row_id, element_id=i) for i in range(num_elements)
        ]


class FieldFakeStructStruct(StructField):
    f_scalar: Final[type["FieldFakeStructStructScalar"]]

    @classmethod
    def get_value(cls, *, row_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeStructStructScalar.get_value(row_id=row_id),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int) -> FieldMap:
        return {
            cls.f_scalar: FieldFakeStructStructScalar.get_value(row_id=row_id),
        }


class FieldFakeSequenceElement(StructField):
    f_scalar: Final[type["FieldFakeSequenceElementScalar"]]

    @classmethod
    def get_value(cls, *, row_id: int, element_id: int) -> Mapping[str, Any]:
        return {
            cls.f_scalar.name: FieldFakeSequenceElementScalar.get_value(row_id=row_id, element_id=element_id),
        }

    @classmethod
    def get_field_mapped_value(cls, *, row_id: int, element_id: int) -> FieldMap:
        return {
            cls.f_scalar: FieldFakeSequenceElementScalar.get_value(row_id=row_id, element_id=element_id),
        }


class FieldFakeStructStructScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int) -> str:
        return f"struct_struct_scalar_{row_id}"


class FieldFakeSequenceElementScalar(ScalarField):
    @classmethod
    def get_value(cls, *, row_id: int, element_id: int) -> str:
        return f"sequence_element_struct_scalar_{row_id}_{element_id}"


DatasetFake.id = "fake_dataset"
DatasetFake.fields = [
    FieldFakeScalar,
    FieldFakeStruct,
    FieldFakeSequence,
]
DatasetFake.f_scalar = FieldFakeScalar
DatasetFake.f_struct = FieldFakeStruct
DatasetFake.f_sequence = FieldFakeSequence

FieldFakeScalar.dataset = DatasetFake
FieldFakeScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeScalar.path = [DatasetFake, FieldFakeScalar]

FieldFakeStruct.dataset = DatasetFake
FieldFakeStruct.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeStruct.name = STRUCT_TYPE_FIELD_NAME
FieldFakeStruct.path = [DatasetFake, FieldFakeStruct]
FieldFakeStruct.fields = [FieldFakeStructStruct]
FieldFakeStruct.f_struct = FieldFakeStructStruct

FieldFakeSequence.dataset = DatasetFake
FieldFakeSequence.data_type = OpenTargetsDatasetFieldType.ARRAY
FieldFakeSequence.name = SEQUENCE_TYPE_FIELD_NAME
FieldFakeSequence.path = [DatasetFake, FieldFakeSequence]
FieldFakeSequence.element = FieldFakeSequenceElement

FieldFakeStructStruct.dataset = DatasetFake
FieldFakeStructStruct.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeStructStruct.name = STRUCT_TYPE_FIELD_NAME
FieldFakeStructStruct.path = [DatasetFake, FieldFakeStruct, FieldFakeStructStruct]
FieldFakeStructStruct.fields = [FieldFakeStructStructScalar]
FieldFakeStructStruct.f_scalar = FieldFakeStructStructScalar

FieldFakeSequenceElement.dataset = DatasetFake
FieldFakeSequenceElement.data_type = OpenTargetsDatasetFieldType.STRUCT
FieldFakeSequenceElement.name = "element"
FieldFakeSequenceElement.path = [DatasetFake, FieldFakeSequence, FieldFakeSequenceElement]
FieldFakeSequenceElement.fields = [FieldFakeSequenceElementScalar]
FieldFakeSequenceElement.f_scalar = FieldFakeSequenceElementScalar

FieldFakeStructStructScalar.dataset = DatasetFake
FieldFakeStructStructScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeStructStructScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeStructStructScalar.path = [DatasetFake, FieldFakeStruct, FieldFakeStructStruct, FieldFakeStructStructScalar]

FieldFakeSequenceElementScalar.dataset = DatasetFake
FieldFakeSequenceElementScalar.data_type = OpenTargetsDatasetFieldType.STRING
FieldFakeSequenceElementScalar.name = SCALAR_TYPE_FIELD_NAME
FieldFakeSequenceElementScalar.path = [
    DatasetFake,
    FieldFakeSequence,
    FieldFakeSequenceElement,
    FieldFakeSequenceElementScalar,
]
