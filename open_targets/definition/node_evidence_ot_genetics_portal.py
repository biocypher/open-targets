"""Acquisition definition that acquires nodes of Open Targets Genetics Portal evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBeta,
    FieldEvidenceBetaConfidenceIntervalLower,
    FieldEvidenceBetaConfidenceIntervalUpper,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceOddsRatio,
    FieldEvidenceOddsRatioConfidenceIntervalLower,
    FieldEvidenceOddsRatioConfidenceIntervalUpper,
    FieldEvidenceProjectId,
    FieldEvidencePublicationFirstAuthor,
    FieldEvidencePublicationYear,
    FieldEvidencePValueExponent,
    FieldEvidencePValueMantissa,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceStudySampleSize,
    FieldEvidenceVariantEffect,
    FieldEvidenceVariantFunctionalConsequenceFromQtlId,
    FieldEvidenceVariantFunctionalConsequenceId,
    FieldEvidenceVariantId,
    FieldEvidenceVariantRsId,
)

node_evidence_ot_genetics_portal: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'ot_genetics_portal'",
    ),
    primary_id=FieldEvidenceId,
    label="OT_GENETICS_PORTAL_EVIDENCE",
    properties=[
        FieldEvidenceBeta,
        FieldEvidenceBetaConfidenceIntervalLower,
        FieldEvidenceBetaConfidenceIntervalUpper,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceLiterature,
        FieldEvidenceOddsRatio,
        FieldEvidenceOddsRatioConfidenceIntervalLower,
        FieldEvidenceOddsRatioConfidenceIntervalUpper,
        FieldEvidencePValueExponent,
        FieldEvidencePValueMantissa,
        FieldEvidenceProjectId,
        FieldEvidencePublicationFirstAuthor,
        FieldEvidencePublicationYear,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceStudySampleSize,
        FieldEvidenceVariantEffect,
        FieldEvidenceVariantFunctionalConsequenceFromQtlId,
        FieldEvidenceVariantFunctionalConsequenceId,
        FieldEvidenceVariantId,
        FieldEvidenceVariantRsId,
    ],
)
