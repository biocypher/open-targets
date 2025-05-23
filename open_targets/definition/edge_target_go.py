"""Acquisition definition that acquires edges between targets and GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
    ToStringExpression,
)
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
from open_targets.definition.curie_prefix import ENSEMBL_PREFIX

edge_target_go: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsGo,
    ),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_PREFIX),
                reference=FieldExpression(FieldTargetsId),
                normalise=True,
            ),
            LiteralExpression("->"),
            NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldTargetsGoElementId))),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldTargetsId),
        normalise=True,
    ),
    target=NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldTargetsGoElementId))),
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
