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
    """Scan operation that returns each row of the dataset."""


@dataclass(frozen=True)
class ExplodingScanOperation(ScanOperation):
    """Scan operation that returns the exploded results.

    This scan operation will explode the fields against the targeted sequence
    type field. Given a table below and the targeted field is colB:

    | colA: str | colB: list[str] | colC: list[str] |
    |-----------|-----------------|-----------------|
    | a         | [b, c]          | [d, e]          |
    | f         | [g, h]          | [i, j]          |

    The output will be:
    | colA: str | colBElement: str | colC: list[str] |
    |-----------|------------------|-----------------|
    | a         | b                | [d, e]          |
    | a         | c                | [d, e]          |
    | f         | g                | [i, j]          |
    | f         | h                | [i, j]          |
    """

    exploded_field: type[SequenceField]
