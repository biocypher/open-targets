"""Acquisition definition that acquires nodes of Expression Atlas evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceBiosamplesFromSource,
    FieldEvidenceConfidence,
    FieldEvidenceContrast,
    FieldEvidenceLiterature,
    FieldEvidenceLog2FoldChangePercentileRank,
    FieldEvidenceLog2FoldChangeValue,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceStudyOverview,
)

node_evidence_expression_atlas: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'expression_atlas'",
    ),
    primary_id=FieldEvidenceId,
    label="EXPRESSION_ATLAS_EVIDENCE",
    properties=[
        FieldEvidenceBiosamplesFromSource,
        FieldEvidenceConfidence,
        FieldEvidenceContrast,
        FieldEvidenceLiterature,
        FieldEvidenceLog2FoldChangePercentileRank,
        FieldEvidenceLog2FoldChangeValue,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceStudyOverview,
    ],
)
