from dataclasses import dataclass

from open_targets.adapter.data_view import DataViewPrimitiveValue
from open_targets.data.schema_base import Field


@dataclass(frozen=True)
class ScanOperationPredicate:
    """Base class for all scan operation predicates.

    The predicate will be used to filter the dataset.
    """


@dataclass(frozen=True)
class PushdownEqualityPredicate(ScanOperationPredicate):
    """Predicate that filters the dataset based on equality.

    The predicate will be run on the data side. The comparand field must be a
    primitive type and not nested.
    """

    field: type[Field]
    value: DataViewPrimitiveValue
