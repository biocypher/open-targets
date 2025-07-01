"""Acquisition definition that acquires edges between targets and diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDiseaseId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetId,
)

edge_target_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceId,
    source=FieldEvidenceTargetId,
    target=FieldEvidenceDiseaseId,
    label="TARGET_TO_DISEASE_ASSOCIATION",
    properties=[
        FieldEvidenceDatasourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
    ],
)
