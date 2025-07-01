"""Acquisition definition that acquires edges between molecules and targets."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDrugId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceDrugId, FieldEvidenceTargetId),
    source=FieldEvidenceDrugId,
    target=FieldEvidenceTargetId,
    label="MOLECULE_TO_TARGET_ASSOCIATION",
    properties=[
        FieldEvidenceDatasourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
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
