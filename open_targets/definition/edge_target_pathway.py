"""Acquisition definition that acquires edges between targets and pathways."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceConfidence,
    FieldEvidencePathways,
    FieldEvidencePathwaysElementId,
    FieldEvidencePublicationFirstAuthor,
    FieldEvidencePublicationYear,
    FieldEvidenceReleaseDate,
    FieldEvidenceReleaseVersion,
    FieldEvidenceResourceScore,
    FieldEvidenceSourceId,
    FieldEvidenceStatisticalMethod,
    FieldEvidenceStatisticalMethodOverview,
    FieldEvidenceTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_pathway: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidencePathways,
    ),
    primary_id=get_arrow_expression(FieldEvidenceTargetId, FieldEvidencePathwaysElementId),
    source=FieldEvidenceTargetId,
    target=FieldEvidencePathwaysElementId,
    label="TARGET_IN_PATHWAY",
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
