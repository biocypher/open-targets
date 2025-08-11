"""Acquisition definition that acquires nodes of SLAPenrich evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidencePathways,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
)

node_evidence_slapenrich: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'slapenrich'",
    ),
    primary_id=FieldEvidenceId,
    label="SLAPENRICH_EVIDENCE",
    properties=[
        FieldEvidenceDiseaseFromSource,
        FieldEvidencePathways,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
    ],
)
