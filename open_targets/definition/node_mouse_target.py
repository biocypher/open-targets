from typing import Final

from open_targets.adapter.generation_definition import (
    GenerationDefinition,
    SimpleNodeGenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldMousePhenotypesTargetFromSourceId,
    FieldMousePhenotypesTargetInModel,
    FieldMousePhenotypesTargetInModelEnsemblId,
    FieldMousePhenotypesTargetInModelMgiId,
)

node_mouse_target: Final[GenerationDefinition[NodeInfo]] = SimpleNodeGenerationDefinition(
    primary_id=FieldMousePhenotypesTargetInModelEnsemblId,
    labels=[],
    properties=[
        FieldMousePhenotypesTargetInModel,
        FieldMousePhenotypesTargetInModelMgiId,
        FieldMousePhenotypesTargetFromSourceId,
    ],
)
