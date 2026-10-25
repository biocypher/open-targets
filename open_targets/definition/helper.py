"""Helper functions for quickly building commonly used expressions."""

from typing import Any, cast, get_args

from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
    StringHashExpression,
    ToStringExpression,
    TransformExpression,
)
from open_targets.data.schema_base import Field


def get_arrow_expression(
    source: Expression[Any] | type[Field],
    target: Expression[Any] | type[Field],
) -> Expression[str]:
    """Get an expression that returns `{source}->{target}`."""
    if isinstance(source, type):
        source = FieldExpression(source)
    if isinstance(target, type):
        target = FieldExpression(target)

    return StringConcatenationExpression(
        expressions=[
            ToStringExpression(source),
            LiteralExpression("->"),
            ToStringExpression(target),
        ],
    )


def get_namespaced_expression(
    namespace: str,
    value_expression: Expression[Any] | type[Field],
) -> Expression[str]:
    """Get an expression that prefixes a string with a namespace.

    This return an expression that produces a string like `namespace::value`.
    This helper automatically converts the value expression to a string if the
    expression is not already a string.
    """
    if isinstance(value_expression, type):
        value_expression = FieldExpression(value_expression)
    args = get_args(type(value_expression))
    if len(args) == 0 or args[0] is not str:
        value_expression = ToStringExpression(value_expression)

    return StringConcatenationExpression(
        expressions=[
            LiteralExpression(f"{namespace}::"),
            value_expression,
        ],
    )


def get_namespaced_hash_expression(
    namespace: str,
    value_expression: Expression[Any] | type[Field],
) -> Expression[str]:
    """Get an expression that hashes a string and prefix it with a namespace.

    This return an expression that produces a string like
    `namespace::hash(value)`. This helper automatically converts the value
    expression to a string if the expression is not already a string.
    """
    if isinstance(value_expression, type):
        value_expression = FieldExpression(value_expression)
    args = get_args(type(value_expression))
    if len(args) == 0 or args[0] is not str:
        value_expression = ToStringExpression(value_expression)

    return get_namespaced_expression(namespace, StringHashExpression(value_expression))


def _null_if_empty_list(value: Any) -> Any:  # noqa: ANN401
    """Return null for an empty list, otherwise the original value."""
    if isinstance(value, list) and not value:
        return None
    return cast("Any", value)


def get_null_if_empty_list_expression(
    value_expression: Expression[Any] | type[Field],
) -> Expression[Any]:
    """Get an expression that turns empty lists into null.

    Neo4j's parquet importer stores empty lists as empty byte arrays. Writing
    null instead of an empty list avoids the resulting `LIST<INTEGER>` type.
    """
    if isinstance(value_expression, type):
        value_expression = FieldExpression(value_expression)
    return TransformExpression(value_expression, _null_if_empty_list)
