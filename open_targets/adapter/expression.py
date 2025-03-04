from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Final, Generic, TypeVar

from open_targets.data.schema_base import Field

TValue = TypeVar("TValue")


class Expression(Generic[TValue]):
    pass


@dataclass(frozen=True)
class FieldExpression(Expression[Any]):
    field: Final[type[Field]]


@dataclass(frozen=True)
class LiteralExpression(Expression[TValue]):
    value: TValue


@dataclass(frozen=True)
class TransformExpression(Expression[TValue]):
    function: Callable[[Any], TValue]


@dataclass(frozen=True)
class ToStringExpression(Expression[str]):
    expression: Expression[Any]


@dataclass(frozen=True)
class StringConcatenationExpression(Expression[str]):
    expressions: Sequence[Expression[Any]]


def recursive_get_dependent_fields(expression: Expression[Any]) -> set[type[Field]]:
    match expression:
        case FieldExpression():
            return {expression.field}
        case ToStringExpression():
            return recursive_get_dependent_fields(expression.expression)
        case StringConcatenationExpression():
            return set[type[Field]].union(*(recursive_get_dependent_fields(e) for e in expression.expressions))
        case _:
            return set()
