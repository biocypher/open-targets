"""Acquisition definition that acquires edges from evidence to biomarkers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiomarkersGeneExpression,
    FieldEvidenceBiomarkersGeneExpressionElementId,
    FieldEvidenceBiomarkersGeneticVariation,
    FieldEvidenceBiomarkersGeneticVariationElementId,
    FieldEvidenceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_biomarker_gene_expression: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetEvidence,
            exploded_field=FieldEvidenceBiomarkersGeneExpression,
        ),
        primary_id=get_arrow_expression(
            FieldEvidenceId,
            BuildCurieExpression(
                prefix=LiteralExpression("gene_expression"),
                reference=FieldExpression(FieldEvidenceBiomarkersGeneExpressionElementId),
            ),
        ),
        source=FieldEvidenceId,
        target=BuildCurieExpression(
            prefix=LiteralExpression("gene_expression"),
            reference=FieldExpression(FieldEvidenceBiomarkersGeneExpressionElementId),
        ),
        label="HAS_BIOMARKER",
        properties=[],
    )
)

edge_evidence_has_biomarker_genetic_variation: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetEvidence,
            exploded_field=FieldEvidenceBiomarkersGeneticVariation,
        ),
        primary_id=get_arrow_expression(
            FieldEvidenceId,
            BuildCurieExpression(
                prefix=LiteralExpression("genetic_variation"),
                reference=FieldExpression(FieldEvidenceBiomarkersGeneticVariationElementId),
            ),
        ),
        source=FieldEvidenceId,
        target=BuildCurieExpression(
            prefix=LiteralExpression("genetic_variation"),
            reference=FieldExpression(FieldEvidenceBiomarkersGeneticVariationElementId),
        ),
        label="HAS_BIOMARKER",
        properties=[],
    )
)
