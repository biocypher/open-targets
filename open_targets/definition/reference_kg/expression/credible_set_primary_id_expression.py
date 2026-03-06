"""Summary: namespaced primary ID for CREDIBLE_SET nodes.

Primary ID expression for CREDIBLE_SET nodes: concatenates 'credible_set_' prefix with
a hash of studyLocusId, fineMappingMethod, and credibleSetIndex.
"""

from typing import Final

from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    StringConcatenationExpression,
    ToStringExpression,
)
from open_targets.data.schema import (
    FieldCredibleSetCredibleSetIndex,
    FieldCredibleSetFinemappingMethod,
    FieldCredibleSetStudyLocusId,
)
from open_targets.definition.helper import get_namespaced_hash_expression

credible_set_primary_id_expression: Final[Expression[str]] = get_namespaced_hash_expression(
    "credible_set",
    StringConcatenationExpression(
        [
            ToStringExpression(FieldExpression(FieldCredibleSetStudyLocusId)),
            ToStringExpression(FieldExpression(FieldCredibleSetFinemappingMethod)),
            ToStringExpression(FieldExpression(FieldCredibleSetCredibleSetIndex)),
        ],
    ),
)
