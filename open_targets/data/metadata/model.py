"""Data models for Open Targets Platform data metadata in JSON."""

from datetime import datetime
from enum import Enum
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class ConfiguredBaseModel(BaseModel):
    """Base model with extra configuration.

    Base model configured to convert names from camel case to snake case and
    ignore unused properties.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )


class _OpenTargetsDatasetFieldType(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    ARRAY = "array"
    STRUCT = "struct"


class _OpenTargetsDatasetArrayTypeModel(ConfiguredBaseModel):
    """Data model of an array type in JSON."""

    type: Literal[_OpenTargetsDatasetFieldType.ARRAY]
    element_type: "FieldTypeDataType"
    contains_null: bool


class _OpenTargetsDatasetStructTypeModel(ConfiguredBaseModel):
    """Data model of a struct type in JSON."""

    type: Literal[_OpenTargetsDatasetFieldType.STRUCT]
    fields: list["_OpenTargetsDatasetFieldModel"]


FieldTypeDataType: TypeAlias = (
    Literal[
        _OpenTargetsDatasetFieldType.BOOLEAN,
        _OpenTargetsDatasetFieldType.INTEGER,
        _OpenTargetsDatasetFieldType.LONG,
        _OpenTargetsDatasetFieldType.FLOAT,
        _OpenTargetsDatasetFieldType.DOUBLE,
        _OpenTargetsDatasetFieldType.STRING,
    ]
    | _OpenTargetsDatasetArrayTypeModel
    | _OpenTargetsDatasetStructTypeModel
)


class _OpenTargetsDatasetFieldModel(ConfiguredBaseModel):
    """Data model of a dataset field in JSON."""

    name: str
    type: FieldTypeDataType
    nullable: bool


class _OpenTargetsDatasetSchemaModel(_OpenTargetsDatasetStructTypeModel):
    pass


class _OpenTargetsDatasetFormat(str, Enum):
    JSON = "json"
    PARQUET = "parquet"


class _OpenTargetsDatasetMetadataResourceModel(ConfiguredBaseModel):
    """Data model of a dataset metadata resource in JSON."""

    format: _OpenTargetsDatasetFormat
    path: str


class _OpenTargetsDatasetMetadataModel(ConfiguredBaseModel):
    """Data model of a dataset metadata in JSON."""

    id: str
    resource: _OpenTargetsDatasetMetadataResourceModel
    dataset_schema: Annotated[_OpenTargetsDatasetSchemaModel, Field(alias="serialisedSchema")]
    time_stamp: datetime

    @field_validator("dataset_schema", mode="before")
    @classmethod
    def deserialise_schema(
        cls: type["_OpenTargetsDatasetMetadataModel"],
        v: str,
    ) -> _OpenTargetsDatasetSchemaModel:
        return _OpenTargetsDatasetSchemaModel.model_validate_json(v)
