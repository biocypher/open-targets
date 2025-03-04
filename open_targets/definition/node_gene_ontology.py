from typing import Final

from open_targets.adapter.generation_definition import ExpressionNodeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldGoId,
    FieldGoName,
)

node_gene_ontology: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    primary_id=FieldGoId,
    labels=[],
    properties=[
        FieldGoName,
    ],
)
