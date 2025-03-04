from abc import ABC
from dataclasses import dataclass

from open_targets.data.schema_base import Dataset, Field


@dataclass(frozen=True)
class ScanOperation(ABC):
    dataset: type[Dataset]


class RowScanOperation(ScanOperation):
    pass


class FlatteningScanOperation(ScanOperation):
    flattened_field: type[Field]
