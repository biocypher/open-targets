"""Acquisition definition that acquires nodes of clinical trials."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceClinicalPhase,
    FieldEvidenceClinicalSignificances,
    FieldEvidenceClinicalStatus,
    FieldEvidenceCohortDescription,
    FieldEvidenceCohortId,
    FieldEvidenceCohortPhenotypes,
    FieldEvidenceCohortShortName,
    FieldEvidenceProjectId,
    FieldEvidenceStudyCases,
    FieldEvidenceStudyCasesWithQualifyingVariants,
    FieldEvidenceStudyId,
    FieldEvidenceStudyOverview,
    FieldEvidenceStudySampleSize,
    FieldEvidenceStudyStartDate,
    FieldEvidenceStudyStopReason,
    FieldEvidenceStudyStopReasonCategories,
)

node_clinical_trial: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceStudyId,
    label="CLINICAL_TRIAL",
    properties=[
        FieldEvidenceClinicalPhase,
        FieldEvidenceClinicalSignificances,
        FieldEvidenceClinicalStatus,
        FieldEvidenceCohortDescription,
        FieldEvidenceCohortId,
        FieldEvidenceCohortPhenotypes,
        FieldEvidenceCohortShortName,
        FieldEvidenceProjectId,
        FieldEvidenceStudyCases,
        FieldEvidenceStudyCasesWithQualifyingVariants,
        FieldEvidenceStudyOverview,
        FieldEvidenceStudySampleSize,
        FieldEvidenceStudyStartDate,
        FieldEvidenceStudyStopReason,
        FieldEvidenceStudyStopReasonCategories,
    ],
)
