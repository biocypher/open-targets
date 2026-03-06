"""Summary: namespaced literature (PMID) IDs for target–target interactions.

Expression that builds a namespaced ID for literature (PubMed ID) supporting
a target–target interaction, using the literature_index namespace.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
)
from open_targets.data.schema import FieldInteractionEvidencePubmedId
from open_targets.definition.helper import get_namespaced_expression

target_target_interaction_literature_entry_expression: Final[Expression[str]] = get_namespaced_expression(
    "literature_entry",
    FieldInteractionEvidencePubmedId,
)
