"""Acquisition definition that acquires edges between targets and GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
)
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetInteraction,
    FieldInteractionCount,
    FieldInteractionScoring,
    FieldInteractionTargetA,
    FieldInteractionTargetB,
)
from open_targets.definition.curie_prefix import ENSEMBL_PREFIX

edge_target_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetInteraction),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_PREFIX),
                reference=FieldExpression(FieldInteractionTargetA),
                normalise=True,
            ),
            LiteralExpression("->"),
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_PREFIX),
                reference=FieldExpression(FieldInteractionTargetB),
                normalise=True,
            ),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldInteractionTargetA),
        normalise=True,
    ),
    target=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldInteractionTargetB),
        normalise=True,
    ),
    label=LiteralExpression("GENE_TO_GENE_INTERACTION"),
    properties=[
        FieldInteractionCount,
        FieldInteractionScoring,
    ],
)
