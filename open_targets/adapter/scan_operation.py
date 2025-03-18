"""Definition of scan operations.

Scan operations describe how to scan through the dataset and the shape of the
returned items of the data stream.
"""

from abc import ABC
from dataclasses import dataclass

from open_targets.data.schema_base import Dataset, SequenceField


@dataclass(frozen=True)
class ScanOperation(ABC):
    """Base class for all scan operations.

    The scan operation will be performed on the set dataset.
    """

    dataset: type[Dataset]


@dataclass(frozen=True)
class RowScanOperation(ScanOperation):
    """Scan operation that scans each row of the dataset."""


@dataclass(frozen=True)
class FlattenedScanOperation(ScanOperation):
    """Scan operation that recursively scans and flattens nested fields.

    On top of RowScanOperation, this scan operation will flatten the fields
    against the targeted sequence type field. Given a table below:
    colA: str colB: list[str] colC: list[str]
    a    [b, c]    [d, e]
    f    [g, h]    [i, j]

    If the targeted flattened field is colC, the output will be:
    1. a, [b, c], d
    2. a, [b, c], e
    3. f, [g, h], i
    4. f, [g, h], j
    """

    flattened_field: type[SequenceField]
