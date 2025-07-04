"""Acquisition definition that acquires edges from target-target associations to interaction evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetInteractionEvidence,
    FieldInteractionEvidenceInteractionIdentifier,
    FieldInteractionEvidenceTargetA,
    FieldInteractionEvidenceTargetB,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_target_has_evidence: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetInteractionEvidence),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldInteractionEvidenceTargetA, FieldInteractionEvidenceTargetB),
        FieldInteractionEvidenceInteractionIdentifier,
    ),
    source=get_arrow_expression(FieldInteractionEvidenceTargetA, FieldInteractionEvidenceTargetB),
    target=FieldInteractionEvidenceInteractionIdentifier,
    label="HAS_INTERACTION_EVIDENCE",
    properties=[],
)
