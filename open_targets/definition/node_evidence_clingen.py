"""Acquisition definition that acquires nodes of ClinGen evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceAllelicRequirements,
    FieldEvidenceConfidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
)

node_evidence_clingen: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "clingen"),
    ),
    primary_id=FieldEvidenceId,
    label="CLINGEN_EVIDENCE",
    properties=[
        FieldEvidenceAllelicRequirements,
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
    ],
)
