from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from open_targets.adapter.expression import Expression


@dataclass(frozen=True)
class MockExpression(Expression):
    pass


@dataclass(frozen=True)
class MockSingleChildExpression(MockExpression):
    expression: Expression[Any]


@dataclass(frozen=True)
class MockMultipleChildrenExpression(MockExpression):
    expressions: Sequence[Expression[Any]]
