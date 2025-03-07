from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields
from typing import Any, Final, Generic, TypeVar, get_origin

from open_targets.data.schema_base import Field

TValue = TypeVar("TValue")


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class StringLowerExpression(Expression[str]):
    expression: Expression[str]


@dataclass(frozen=True)
class BuildCurieExpression(Expression[str]):
    scheme: Expression[Any]
    path: Expression[Any]
    normalised: bool


@dataclass(frozen=True)
class ExtractCurieSchemeExpression(Expression[str]):
    expression: Expression[str]
    normalise: bool = True


@dataclass(frozen=True)
class NormaliseCurieExpression(Expression[str]):
    expression: Expression[str]


@dataclass(frozen=True)
class ExtractSubstringExpression(Expression[str]):
    expression: Expression[str]
    separator: Expression[str]
    index: int


@dataclass(frozen=True)
class DataSourceToLicenceExpression(Expression[str]):
    datasource: Expression[str]


def recursive_get_dependent_fields(
    expression: Expression[Any],
) -> set[type[Field]]:
    if isinstance(expression, FieldExpression):
        return {expression.field}
    dataset_fields = set[type[Field]]()
    for field in fields(expression):
        if get_origin(field.type) is Expression:
            dataset_fields.update(recursive_get_dependent_fields(getattr(expression, field.name)))
    return dataset_fields
