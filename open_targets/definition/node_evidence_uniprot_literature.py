"""Acquisition definition that acquires nodes of UniProt literature evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceConfidence,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetModulation,
)

node_evidence_uniprot_literature: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'uniprot_literature'",
    ),
    primary_id=FieldEvidenceId,
    label="UNIPROT_LITERATURE_EVIDENCE",
    properties=[
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceTargetModulation,
    ],
)
