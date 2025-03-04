from typing import Final

from open_targets.adapter.expression import (
    FieldExpression,
    StringConcatenationExpression,
)
from open_targets.adapter.generation_definition import ExpressionEdgeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.data.schema import (
    FieldTargetsGoElementEvidence,
    FieldTargetsGoElementId,
    FieldTargetsGoElementSource,
    FieldTargetsId,
)

edge_target_go: Final[GenerationDefinition[EdgeInfo]] = ExpressionEdgeGenerationDefinition(
    primary_id=StringConcatenationExpression(
        expressions=[FieldExpression(FieldTargetsId), FieldExpression(FieldTargetsGoElementId)],
    ),
    source=FieldTargetsId,
    target=FieldTargetsGoElementId,
    labels=[],
    properties=[
        FieldTargetsGoElementSource,
        FieldTargetsGoElementEvidence,
    ],
)
