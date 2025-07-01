"""A set of predefined expressions that can be used for acquisition."""

from abc import abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Final, Generic, TypeVar

from open_targets.adapter.data_view import DataViewValue
from open_targets.data.schema_base import Field

TValue = TypeVar("TValue")


@dataclass(frozen=True)
class Expression(Generic[TValue]):
    """Base class for all expressions.

    The type parameter is the returned type of this expression.
    """


class HasDependentExpressionMixin:
    """Mixin for expressions that have dependent expressions."""

    @property
    @abstractmethod
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""


@dataclass(frozen=True)
class FieldExpression(Expression[DataViewValue]):
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
class TransformExpression(HasDependentExpressionMixin, Expression[TValue]):
    """Expression that transforms values using a custom function."""

    expression: Expression[Any] | None
    function: Callable[[Any], TValue]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression] if self.expression else []


@dataclass(frozen=True)
class NewUuidExpression(Expression[str]):
    """Expression that generates a new UUID."""


@dataclass(frozen=True)
class ToStringExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that converts any value to a string."""

    expression: Expression[Any]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression]


@dataclass(frozen=True)
class StringConcatenationExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that concatenates strings."""

    expressions: Sequence[Expression[str]]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return self.expressions


@dataclass(frozen=True)
class StringLowerExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that converts a string to lowercase."""

    expression: Expression[str]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression]


@dataclass(frozen=True)
class BuildCurieExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that builds a CURIE from parts."""

    prefix: Expression[Any]
    reference: Expression[Any]
    normalise: bool = True

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.prefix, self.reference]


@dataclass(frozen=True)
class ExtractCuriePrefixExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that extracts the prefix from a CURIE like string.

    For example, `GO_00000` results into `go`.
    """

    expression: Expression[str]
    normalise: bool = True

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression]


@dataclass(frozen=True)
class NormaliseCurieExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that normalises a CURIE like string.

    For example, `GO_00000` results into `go:00000`.
    """

    expression: Expression[str]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression]


@dataclass(frozen=True)
class ExtractSubstringExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that extracts a substring.

    The string is split by the separator and the substring at the given index is
    returned.
    """

    expression: Expression[str]
    separator: Expression[str]
    index: int

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.expression, self.separator]


@dataclass(frozen=True)
class DataSourceToLicenceExpression(HasDependentExpressionMixin, Expression[str]):
    """Expression that converts a data source to a licence."""

    datasource: Expression[str]

    @property
    def dependents(self) -> Sequence[Expression[Any]]:
        """The dependent expressions."""
        return [self.datasource]
