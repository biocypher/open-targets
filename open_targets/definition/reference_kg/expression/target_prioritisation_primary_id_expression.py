"""Summary: namespaced primary IDs for target_prioritisation nodes.

Expression that builds a namespaced ID for target_prioritisation
from the Target Engine datasets using the target_prioritisation
namespace.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
)
from open_targets.data.schema import FieldTargetPrioritisationTargetId
from open_targets.definition.helper import get_namespaced_expression

target_prioritisation_primary_id_expression: Final[Expression[str]] = get_namespaced_expression(
    "target_prioritisation",
    FieldTargetPrioritisationTargetId,
)
