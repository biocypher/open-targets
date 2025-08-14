"""Acquisition definition that acquires nodes of Gene2Phenotype evidence."""

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
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceVariantEffect,
    FieldEvidenceVariantFunctionalConsequenceId,
)

node_evidence_gene2phenotype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "gene2phenotype"),
    ),
    primary_id=FieldEvidenceId,
    label="GENE2PHENOTYPE_EVIDENCE",
    properties=[
        FieldEvidenceAllelicRequirements,
        FieldEvidenceConfidence,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceVariantEffect,
        FieldEvidenceVariantFunctionalConsequenceId,
    ],
)
