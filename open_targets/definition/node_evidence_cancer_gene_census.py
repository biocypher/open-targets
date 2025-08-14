"""Acquisition definition that acquires nodes of Cancer Gene Census evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceId,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceVariantEffect,
)

node_evidence_cancer_gene_census: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "cancer_gene_census"),
    ),
    primary_id=FieldEvidenceId,
    label="CANCER_GENE_CENSUS_EVIDENCE",
    properties=[
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceVariantEffect,
    ],
)
