"""Acquisition definition that acquires edges from evidence to drugs."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDrugId,
    FieldEvidenceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_drug: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceDrugId),
    source=FieldEvidenceId,
    target=FieldEvidenceDrugId,
    label="HAS_DRUG",
    properties=[],
)
