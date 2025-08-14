"""Acquisition definition that acquires nodes of ChEMBL evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceClinicalPhase,
    FieldEvidenceClinicalStatus,
    FieldEvidenceCohortPhenotypes,
    FieldEvidenceDatasourceId,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDrugId,
    FieldEvidenceId,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceStudyStartDate,
    FieldEvidenceStudyStopReason,
    FieldEvidenceStudyStopReasonCategories,
    FieldEvidenceTargetFromSource,
    FieldEvidenceVariantEffect,
)

node_evidence_chembl: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "chembl"),
    ),
    primary_id=FieldEvidenceId,
    label="CHEMBL_EVIDENCE",
    properties=[
        FieldEvidenceClinicalPhase,
        FieldEvidenceClinicalStatus,
        FieldEvidenceCohortPhenotypes,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDrugId,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceStudyStartDate,
        FieldEvidenceStudyStopReason,
        FieldEvidenceStudyStopReasonCategories,
        FieldEvidenceTargetFromSource,
        FieldEvidenceVariantEffect,
    ],
)
