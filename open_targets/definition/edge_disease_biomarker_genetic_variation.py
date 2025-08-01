"""Acquisition definition that acquires edges between diseases and genetic variation biomarkers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiomarkersGeneticVariation,
    FieldEvidenceBiomarkersGeneticVariationElementId,
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

edge_disease_biomarker_genetic_variation: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceBiomarkersGeneticVariation,
    ),
    primary_id=get_arrow_expression(
        FieldEvidenceDiseaseId,
        BuildCurieExpression(
            prefix=LiteralExpression("genetic_variation"),
            reference=FieldExpression(FieldEvidenceBiomarkersGeneticVariationElementId),
        ),
    ),
    source=FieldEvidenceDiseaseId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("genetic_variation"),
        reference=FieldExpression(FieldEvidenceBiomarkersGeneticVariationElementId),
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
