"""Acquisition definition that acquires nodes of CRISPR evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceDiseaseCellLines,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceLiterature,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceTargetFromSource,
)

node_evidence_crispr: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'crispr'",
    ),
    primary_id=FieldEvidenceId,
    label="CRISPR_EVIDENCE",
    properties=[
        FieldEvidenceDiseaseCellLines,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceLiterature,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceTargetFromSource,
    ],
)
