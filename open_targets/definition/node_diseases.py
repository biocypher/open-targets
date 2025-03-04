from typing import Final

from open_targets.adapter.generation_definition import ExpressionNodeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldDiseasesCode,
    FieldDiseasesDescription,
    FieldDiseasesId,
    FieldDiseasesName,
)

node_diseases: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    primary_id=FieldDiseasesId,
    labels=[],
    properties=[
        FieldDiseasesCode,
        FieldDiseasesDescription,
        FieldDiseasesName,
    ],
)
