"""Acquisition definition that acquires nodes of SysBio evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceLiterature,
    FieldEvidencePathways,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceStudyOverview,
)

node_evidence_sysbio: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'sysbio'",
    ),
    primary_id=FieldEvidenceId,
    label="SYSBIO_EVIDENCE",
    properties=[
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceLiterature,
        FieldEvidencePathways,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceStudyOverview,
    ],
)
