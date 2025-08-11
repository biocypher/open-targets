"""Acquisition definition that acquires edges from targets to evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_association_evidence: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceTargetId, FieldEvidenceId),
    source=FieldEvidenceTargetId,
    target=FieldEvidenceId,
    label="HAS_ASSOCIATION_EVIDENCE",
    properties=[],
)
