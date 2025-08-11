"""Acquisition definition that acquires edges from evidence to diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceDiseaseId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_for_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceDiseaseId),
    source=FieldEvidenceId,
    target=FieldEvidenceDiseaseId,
    label="EVIDENCE_FOR_DISEASE",
    properties=[],
)
