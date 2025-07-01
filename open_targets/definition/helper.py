from typing import Any

from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
    ToStringExpression,
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
