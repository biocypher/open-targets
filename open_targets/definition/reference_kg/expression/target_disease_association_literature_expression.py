"""Summary: namespaced literature (PMID) IDs for target-disease associations.

Expression that builds a namespaced ID for literature (PMID) supporting a
target–disease association, using the literature_index namespace.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
)
from open_targets.data.schema import FieldEvidenceCancerBiomarkersLiterature
from open_targets.definition.helper import get_namespaced_expression

target_disease_association_literature_entry_expression: Final[Expression[str]] = get_namespaced_expression(
    "literature_index",
    FieldEvidenceCancerBiomarkersLiterature,
)
