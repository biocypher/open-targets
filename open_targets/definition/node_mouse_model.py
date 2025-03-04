from typing import Final

from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldMousePhenotypesBiologicalModels,
    FieldMousePhenotypesModelPhenotypeClasses,
)

node_mouse_model: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    primary_id=FieldMousePhenotypesBiologicalModels,
    labels=[],
    properties=[
        FieldMousePhenotypesModelPhenotypeClasses,
    ],
)
