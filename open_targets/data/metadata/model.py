"""Data models for Open Targets Platform data metadata in JSON."""

from datetime import datetime
from enum import Enum
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class ConfiguredBaseModel(BaseModel):
    """Base model with extra configuration.

    Base model configured to convert names from camel case used in JSON to snake
    case used in Python and ignore unused properties.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )


class OpenTargetsDatasetFieldType(str, Enum):
    """Data type of a dataset field."""

    BOOLEAN = "boolean"
    INTEGER = "integer"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    ARRAY = "array"
    MAP = "map"
    STRUCT = "struct"


class OpenTargetsDatasetArrayTypeModel(ConfiguredBaseModel):
    """Data model of an array type in JSON."""

    type: Literal[OpenTargetsDatasetFieldType.ARRAY]
    element_type: "OpenTargetsDatasetFieldModelTypeModel"
    contains_null: bool


class OpenTargetsDatasetMapTypeModel(ConfiguredBaseModel):
    """Data model of a map type in JSON."""

    type: Literal[OpenTargetsDatasetFieldType.MAP]
    key_type: "OpenTargetsDatasetFieldModelTypeModel"
    value_type: "OpenTargetsDatasetFieldModelTypeModel"
    value_contains_null: bool


class OpenTargetsDatasetStructTypeModel(ConfiguredBaseModel):
    """Data model of a struct type in JSON."""

    type: Literal[OpenTargetsDatasetFieldType.STRUCT]
    fields: list["OpenTargetsDatasetFieldModel"]


OpenTargetsDatasetFieldTypePrimitiveSet: TypeAlias = Literal[
    OpenTargetsDatasetFieldType.BOOLEAN,
    OpenTargetsDatasetFieldType.INTEGER,
    OpenTargetsDatasetFieldType.LONG,
    OpenTargetsDatasetFieldType.FLOAT,
    OpenTargetsDatasetFieldType.DOUBLE,
    OpenTargetsDatasetFieldType.STRING,
]

OpenTargetsDatasetFieldTypeComplexSet: TypeAlias = Literal[
    OpenTargetsDatasetFieldType.ARRAY,
    OpenTargetsDatasetFieldType.MAP,
    OpenTargetsDatasetFieldType.STRUCT,
]

OpenTargetsDatasetComplexTypeModel: TypeAlias = (
    OpenTargetsDatasetArrayTypeModel | OpenTargetsDatasetMapTypeModel | OpenTargetsDatasetStructTypeModel
)

OpenTargetsDatasetFieldModelTypeModel: TypeAlias = (
    OpenTargetsDatasetFieldTypePrimitiveSet | OpenTargetsDatasetComplexTypeModel
)


class OpenTargetsDatasetFieldModel(ConfiguredBaseModel):
    """Data model of a dataset field in JSON."""

    name: str
    type: OpenTargetsDatasetFieldModelTypeModel
    nullable: bool


class OpenTargetsDatasetSchemaModel(OpenTargetsDatasetStructTypeModel):
    """Data model of a dataset schema in JSON."""


class OpenTargetsDatasetFormat(str, Enum):
    """Data format of a dataset."""

    JSON = "json"
    PARQUET = "parquet"


class OpenTargetsDatasetResourceModel(ConfiguredBaseModel):
    """Data model of a dataset metadata resource in JSON."""

    format: OpenTargetsDatasetFormat
    path: str


class OpenTargetsDatasetMetadataModel(ConfiguredBaseModel):
    """Data model of a dataset metadata in JSON."""

    id: str
    resource: OpenTargetsDatasetResourceModel
    dataset_schema: Annotated[OpenTargetsDatasetSchemaModel, Field(alias="serialisedSchema")]
    time_stamp: datetime

    @field_validator("dataset_schema", mode="before")
    @classmethod
    def _deserialise_schema(
        cls: type["OpenTargetsDatasetMetadataModel"],
        v: str,
    ) -> OpenTargetsDatasetSchemaModel:
        return OpenTargetsDatasetSchemaModel.model_validate_json(v)
