"""Acquisition definition that acquires edges from evidence to variants."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceVariantId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_variant: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceVariantId),
    source=FieldEvidenceId,
    target=FieldEvidenceVariantId,
    label="HAS_VARIANT",
    properties=[],
)
