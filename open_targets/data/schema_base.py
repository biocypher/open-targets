# ruff: noqa: PGH003
# type: ignore

from abc import ABC
from collections.abc import Sequence
from typing import Final

from open_targets.data.metadata.model import OpenTargetsDatasetFieldType


class Dataset:
    id: Final[str]
    fields: Final[Sequence[type["Field"]]]


class Field(ABC):
    name: Final[str]
    data_type: Final[OpenTargetsDatasetFieldType]
    dataset: Final[type["Dataset"]]
    path: Final[Sequence[type["Dataset"] | type["Field"]]]
    nullable: Final[bool]


class ScalarField(Field):
    pass


class StructField(Field):
    fields: Final[Sequence[type["Field"]]]


class SequenceField(Field):
    element: Final[type["Field"]]


class MapField(Field):
    key: Final[type["Field"]]
    value: Final[type["Field"]]
