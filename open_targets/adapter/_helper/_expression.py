from typing import Any, TypeAlias

from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    HasDependentExpressionMixin,
    LiteralExpression,
)
from open_targets.data.schema_base import Field

Source: TypeAlias = int | float | str | type[Field] | Expression[Any]


def to_expression(value: Source) -> Expression[Any]:
    if isinstance(value, Expression):
        return value
    if isinstance(value, type):
        return FieldExpression(value)
    return LiteralExpression(value)


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
    if isinstance(expression, HasDependentExpressionMixin):
        for child in expression.dependents:
            dataset_fields.update(recursive_get_dependent_fields(child))
    return dataset_fields
