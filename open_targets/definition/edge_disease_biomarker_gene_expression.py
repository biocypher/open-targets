"""Acquisition definition that acquires edges between diseases and gene expression biomarkers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiomarkersGeneExpression,
    FieldEvidenceBiomarkersGeneExpressionElementId,
    FieldEvidenceConfidence,
    FieldEvidenceDiseaseId,
    FieldEvidencePublicationFirstAuthor,
    FieldEvidencePublicationYear,
    FieldEvidenceReleaseDate,
    FieldEvidenceReleaseVersion,
    FieldEvidenceResourceScore,
    FieldEvidenceSourceId,
    FieldEvidenceStatisticalMethod,
    FieldEvidenceStatisticalMethodOverview,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_biomarker_gene_expression: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceBiomarkersGeneExpression,
    ),
    primary_id=get_arrow_expression(
        FieldEvidenceDiseaseId,
        BuildCurieExpression(
            prefix=LiteralExpression("gene_expression"),
            reference=FieldExpression(FieldEvidenceBiomarkersGeneExpressionElementId),
        ),
    ),
    source=FieldEvidenceDiseaseId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("gene_expression"),
        reference=FieldExpression(FieldEvidenceBiomarkersGeneExpressionElementId),
    ),
    label="DISEASE_HAS_BIOMARKER",
    properties=[
        FieldEvidenceConfidence,
        FieldEvidenceResourceScore,
        FieldEvidenceReleaseDate,
        FieldEvidenceReleaseVersion,
        FieldEvidenceSourceId,
        FieldEvidenceStatisticalMethod,
        FieldEvidenceStatisticalMethodOverview,
        FieldEvidencePublicationFirstAuthor,
        FieldEvidencePublicationYear,
    ],
)
