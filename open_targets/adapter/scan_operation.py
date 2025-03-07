from abc import ABC
from dataclasses import dataclass

from open_targets.data.schema_base import Dataset, Field


@dataclass(frozen=True)
class ScanOperation(ABC):
    dataset: type[Dataset]


@dataclass(frozen=True)
class RowScanOperation(ScanOperation):
    pass


@dataclass(frozen=True)
class FlattenedScanOperation(ScanOperation):
    flattened_field: type[Field]
