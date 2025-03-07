from typing import Final

from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
)
from open_targets.adapter.generation_definition import ExpressionEdgeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import FlattenedScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsGo,
    FieldTargetsGoElementAspect,
    FieldTargetsGoElementEcoId,
    FieldTargetsGoElementEvidence,
    FieldTargetsGoElementGeneProduct,
    FieldTargetsGoElementId,
    FieldTargetsGoElementSource,
    FieldTargetsId,
)
from open_targets.definition.node_targets import _TYPE

edge_target_go: Final[GenerationDefinition[EdgeInfo]] = ExpressionEdgeGenerationDefinition(
    scan_operation=FlattenedScanOperation(
        dataset=DatasetTargets,
        flattened_field=FieldTargetsGo,
    ),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                scheme=LiteralExpression(_TYPE),
                path=FieldExpression(FieldTargetsId),
                normalised=True,
            ),
            LiteralExpression("->"),
            NormaliseCurieExpression(FieldExpression(FieldTargetsGoElementId)),
        ],
    ),
    source=BuildCurieExpression(
        scheme=LiteralExpression(_TYPE),
        path=FieldExpression(FieldTargetsId),
        normalised=True,
    ),
    target=NormaliseCurieExpression(FieldExpression(FieldTargetsGoElementId)),
    labels=[LiteralExpression("GENE_TO_GO_TERM_ASSOCIATION")],
    properties=[
        FieldTargetsGoElementSource,
        FieldTargetsGoElementEvidence,
        FieldTargetsGoElementEcoId,
        FieldTargetsGoElementAspect,
        FieldTargetsGoElementGeneProduct,
    ],
)
