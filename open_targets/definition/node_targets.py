from typing import Final

from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldTargetsApprovedSymbol,
    FieldTargetsBiotype,
    FieldTargetsId,
)

node_targets: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    primary_id=FieldTargetsId,
    labels=[],
    properties=[
        FieldTargetsApprovedSymbol,
        FieldTargetsBiotype,
    ],
)
