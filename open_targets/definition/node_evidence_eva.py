"""Acquisition definition that acquires nodes of EVA evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceAlleleOrigins,
    FieldEvidenceAllelicRequirements,
    FieldEvidenceClinicalSignificances,
    FieldEvidenceCohortPhenotypes,
    FieldEvidenceConfidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceReleaseDate,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceVariantEffect,
    FieldEvidenceVariantFunctionalConsequenceId,
    FieldEvidenceVariantHgvsId,
    FieldEvidenceVariantId,
    FieldEvidenceVariantRsId,
)

node_evidence_eva: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "eva"),
    ),
    primary_id=FieldEvidenceId,
    label="EVA_EVIDENCE",
    properties=[
        FieldEvidenceAlleleOrigins,
        FieldEvidenceAllelicRequirements,
        FieldEvidenceClinicalSignificances,
        FieldEvidenceCohortPhenotypes,
        FieldEvidenceConfidence,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceReleaseDate,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceVariantEffect,
        FieldEvidenceVariantFunctionalConsequenceId,
        FieldEvidenceVariantHgvsId,
        FieldEvidenceVariantId,
        FieldEvidenceVariantRsId,
    ],
)
