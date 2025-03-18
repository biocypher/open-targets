"""Generation definitions for nodes of mouse targets."""

from typing import Final

from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesTargetFromSourceId,
    FieldMousePhenotypesTargetInModel,
    FieldMousePhenotypesTargetInModelEnsemblId,
    FieldMousePhenotypesTargetInModelMgiId,
)
from open_targets.definition.curie_scheme import ENSEMBL_SCHEME
from open_targets.definition.node_shared import node_static_properties

node_mouse_target: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=BuildCurieExpression(
        scheme=LiteralExpression(ENSEMBL_SCHEME),
        path=FieldExpression(FieldMousePhenotypesTargetInModelEnsemblId),
        normalised=True,
    ),
    label="mouse gene",
    properties=[
        FieldMousePhenotypesTargetInModel,
        FieldMousePhenotypesTargetInModelMgiId,
        FieldMousePhenotypesTargetFromSourceId,
        *node_static_properties,
    ],
)
