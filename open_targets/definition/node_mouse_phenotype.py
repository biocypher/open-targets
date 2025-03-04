from typing import Final

from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldMousePhenotypesModelPhenotypeId,
    FieldMousePhenotypesModelPhenotypeLabel,
)

node_mouse_phenotype: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    primary_id=FieldMousePhenotypesModelPhenotypeId,
    labels=[],
    properties=[
        FieldMousePhenotypesModelPhenotypeLabel,
    ],
)
