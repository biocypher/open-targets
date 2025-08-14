"""Acquisition definition that acquires nodes of CRISPR Screen evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceCellType,
    FieldEvidenceContrast,
    FieldEvidenceCrisprScreenLibrary,
    FieldEvidenceDatasourceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceGeneticBackground,
    FieldEvidenceId,
    FieldEvidenceLog2FoldChangeValue,
    FieldEvidenceProjectId,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceStatisticalTestTail,
    FieldEvidenceStudyId,
    FieldEvidenceStudyOverview,
)

node_evidence_crispr_screen: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "crispr_screen"),
    ),
    primary_id=FieldEvidenceId,
    label="CRISPR_SCREEN_EVIDENCE",
    properties=[
        FieldEvidenceCellType,
        FieldEvidenceContrast,
        FieldEvidenceCrisprScreenLibrary,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceGeneticBackground,
        FieldEvidenceLog2FoldChangeValue,
        FieldEvidenceProjectId,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceStatisticalTestTail,
        FieldEvidenceStudyId,
        FieldEvidenceStudyOverview,
    ],
)
