from typing import Final

from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsApprovedSymbol,
    FieldTargetsBiotype,
    FieldTargetsId,
)
from open_targets.definition.curie_scheme import ENSEMBL_SCHEME
from open_targets.definition.node_shared import node_static_properties

node_targets: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargets),
    primary_id=BuildCurieExpression(
        scheme=LiteralExpression(ENSEMBL_SCHEME),
        path=FieldExpression(FieldTargetsId),
        normalised=True,
    ),
    label=ENSEMBL_SCHEME,
    properties=[
        FieldTargetsApprovedSymbol,
        FieldTargetsBiotype,
        *node_static_properties,
    ],
)
