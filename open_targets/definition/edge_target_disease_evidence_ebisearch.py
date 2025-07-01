"""Acquisition definition that acquires edges between targets and diseases from Ebisearch Evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEbisearchEvidence,
    FieldEbisearchEvidenceApprovedSymbol,
    FieldEbisearchEvidenceDiseaseId,
    FieldEbisearchEvidenceName,
    FieldEbisearchEvidenceScore,
    FieldEbisearchEvidenceTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_evidence_ebisearch: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEbisearchEvidence),
    primary_id=get_arrow_expression(FieldEbisearchEvidenceTargetId, FieldEbisearchEvidenceDiseaseId),
    source=FieldEbisearchEvidenceTargetId,
    target=FieldEbisearchEvidenceDiseaseId,
    label="TARGET_TO_DISEASE_EVIDENCE_EBISearch",
    properties=[
        FieldEbisearchEvidenceApprovedSymbol,
        FieldEbisearchEvidenceName,
        FieldEbisearchEvidenceScore,
    ],
)
