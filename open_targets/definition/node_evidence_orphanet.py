"""Acquisition definition that acquires nodes of Orphanet evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceAlleleOrigins,
    FieldEvidenceConfidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetFromSource,
    FieldEvidenceVariantEffect,
    FieldEvidenceVariantFunctionalConsequenceId,
)

node_evidence_orphanet: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "orphanet"),
    ),
    primary_id=FieldEvidenceId,
    label="ORPHANET_EVIDENCE",
    properties=[
        FieldEvidenceAlleleOrigins,
        FieldEvidenceConfidence,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceTargetFromSource,
        FieldEvidenceVariantEffect,
        FieldEvidenceVariantFunctionalConsequenceId,
    ],
)
