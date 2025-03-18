"""Definition of expressions."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields
from typing import Any, Final, Generic, TypeVar, get_origin

from open_targets.data.schema_base import Field

TValue = TypeVar("TValue")


@dataclass(frozen=True)
class Expression(Generic[TValue]):
    """Base class for all expressions.

    The type parameter is the returned type of this expression.
    """


@dataclass(frozen=True)
class FieldExpression(Expression[Any]):
    """Expression that retrives values from a field.

    This is one of the leaf expressions that provides the source of data down to
    the expression chain.
    """

    field: Final[type[Field]]


@dataclass(frozen=True)
class LiteralExpression(Expression[TValue]):
    """Expression that provides a literal value.

    This is one of the leaf expressions that provides the source of data down to
    the expression chain.
    """

    value: TValue


@dataclass(frozen=True)
class TransformExpression(Expression[TValue]):
    """Expression that transforms values using a custom function."""

    function: Callable[[Any], TValue]


@dataclass(frozen=True)
class ToStringExpression(Expression[str]):
    """Expression that converts any value to a string."""

    expression: Expression[Any]


@dataclass(frozen=True)
class StringConcatenationExpression(Expression[str]):
    """Expression that concatenates strings."""

    expressions: Sequence[Expression[Any]]


@dataclass(frozen=True)
class StringLowerExpression(Expression[str]):
    """Expression that converts a string to lowercase."""

    expression: Expression[str]


@dataclass(frozen=True)
class BuildCurieExpression(Expression[str]):
    """Expression that builds a CURIE from parts."""

    scheme: Expression[Any]
    path: Expression[Any]
    normalised: bool = True


@dataclass(frozen=True)
class ExtractCurieSchemeExpression(Expression[str]):
    """Expression that extracts the scheme from a CURIE like string.

    For example, `GO_00000` results into `go`.
    """

    expression: Expression[str]
    normalise: bool = True


@dataclass(frozen=True)
class NormaliseCurieExpression(Expression[str]):
    """Expression that normalises a CURIE like string.

    For example, `GO_00000` results into `go:00000`.
    """

    expression: Expression[str]


@dataclass(frozen=True)
class ExtractSubstringExpression(Expression[str]):
    """Expression that extracts a substring.

    The string is split by the separator and the substring at the given index is
    returned.
    """

    expression: Expression[str]
    separator: Expression[str]
    index: int


@dataclass(frozen=True)
class DataSourceToLicenceExpression(Expression[str]):
    """Expression that converts a data source to a licence."""

    datasource: Expression[str]


def recursive_get_dependent_fields(
    expression: Expression[Any],
) -> set[type[Field]]:
    """Get all dataset fields that an expression depends on.

    This is used to determine the dataset fields that need to be referenced to
    fulfill the expression.
    """
    if isinstance(expression, FieldExpression):
        return {expression.field}
    dataset_fields = set[type[Field]]()
    for field in fields(expression):
        if get_origin(field.type) is Expression:
            dataset_fields.update(recursive_get_dependent_fields(getattr(expression, field.name)))
    return dataset_fields
