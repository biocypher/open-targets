"""Generation definitions for edges between targets and GO terms."""

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
from open_targets.adapter.scan_operation import ExplodingScanOperation
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
from open_targets.definition.curie_scheme import ENSEMBL_SCHEME

edge_target_go: Final[GenerationDefinition[EdgeInfo]] = ExpressionEdgeGenerationDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsGo,
    ),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_SCHEME),
                reference=FieldExpression(FieldTargetsId),
                normalised=True,
            ),
            LiteralExpression("->"),
            NormaliseCurieExpression(FieldExpression(FieldTargetsGoElementId)),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_SCHEME),
        reference=FieldExpression(FieldTargetsId),
        normalised=True,
    ),
    target=NormaliseCurieExpression(FieldExpression(FieldTargetsGoElementId)),
    label=LiteralExpression("GENE_TO_GO_TERM_ASSOCIATION"),
    properties=[
        FieldTargetsGoElementSource,
        FieldTargetsGoElementEvidence,
        FieldTargetsGoElementEcoId,
        FieldTargetsGoElementAspect,
        FieldTargetsGoElementGeneProduct,
        ("licence", "test"),
    ],
)
