"""Summary: namespaced primary ID for COLOCALISATION nodes.

Primary ID expression for COLOCALISATION nodes: concatenates 'coloc_' prefix with
a hash of the left and right StudyLocus IDs to create a stable, namespaced identifier.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    StringConcatenationExpression,
    ToStringExpression,
)
from open_targets.data.schema import (
    FieldColocalisationLeftStudyLocusId,
    FieldColocalisationRightStudyLocusId,
)
from open_targets.definition.helper import get_namespaced_hash_expression

colocalisation_primary_id_expression: Final[Expression[str]] = get_namespaced_hash_expression(
    "colocalisation",
    StringConcatenationExpression(
        [
            ToStringExpression(FieldExpression(FieldColocalisationLeftStudyLocusId)),
            ToStringExpression(FieldExpression(FieldColocalisationRightStudyLocusId)),
        ],
    ),
)
