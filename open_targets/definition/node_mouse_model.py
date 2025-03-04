from typing import Final

from open_targets.adapter.generation_definition import (
    GenerationDefinition,
    SimpleNodeGenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldMousePhenotypesBiologicalModels,
    FieldMousePhenotypesModelPhenotypeClasses,
)

node_mouse_model: Final[GenerationDefinition[NodeInfo]] = SimpleNodeGenerationDefinition(
    primary_id=FieldMousePhenotypesBiologicalModels,
    labels=[],
    properties=[
        FieldMousePhenotypesModelPhenotypeClasses,
    ],
)
