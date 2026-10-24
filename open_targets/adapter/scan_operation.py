"""Scan operations for data acquisition.

Scan operations describe how to scan through the dataset and the shape of the
returned items of the data stream.
"""

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass

from open_targets.adapter.scan_operation_predicate import ScanOperationPredicateExpression
from open_targets.data.schema_base import Dataset, Field, SequenceField, StructField


@dataclass(frozen=True, kw_only=True)
class ScanOperation(ABC):
    """Base class for all scan operations.

    The scan operation will be performed on the set dataset.
    """

    dataset: type[Dataset]
    predicate: ScanOperationPredicateExpression | None = None


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

    Nested exploding is NOT yet supported.

    Null sequences and null elements are skipped by default. Set
    ``drop_null_elements=False`` to keep null elements, or provide a sequence
    of fields under the exploded struct to drop elements when any of those
    fields is null.
    """

    exploded_field: type[SequenceField]
    drop_null_elements: bool | Sequence[type[Field]] = True

    def __post_init__(self) -> None:
        """Validate field-based null dropping."""
        if isinstance(self.drop_null_elements, bool):
            return
        if not issubclass(self.exploded_field.element, StructField):
            msg = "Field-based drop_null_elements requires a struct element"
            raise TypeError(msg)
        for field in self.drop_null_elements:
            if field.path[: len(self.exploded_field.path)] != self.exploded_field.path:
                msg = f"Field {field.__name__} is not under {self.exploded_field.__name__}"
                raise TypeError(msg)
