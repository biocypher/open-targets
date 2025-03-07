from typing import Final

from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesBiologicalModels,
    FieldMousePhenotypesModelPhenotypeClasses,
)
from open_targets.definition.node_shared import node_static_properties

node_mouse_model: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=FieldMousePhenotypesBiologicalModels,
    labels=[],
    properties=[
        FieldMousePhenotypesModelPhenotypeClasses,
        *node_static_properties,
    ],
)
