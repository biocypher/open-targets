"""Acquisition definition that acquires nodes of Reactome evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidencePathways,
    FieldEvidenceReactionId,
    FieldEvidenceReactionName,
    FieldEvidenceScore,
    FieldEvidenceTargetModulation,
    FieldEvidenceVariantAminoacidDescriptions,
)

node_evidence_reactome: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'reactome'",
    ),
    primary_id=FieldEvidenceId,
    label="REACTOME_EVIDENCE",
    properties=[
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidencePathways,
        FieldEvidenceReactionId,
        FieldEvidenceReactionName,
        FieldEvidenceScore,
        FieldEvidenceTargetModulation,
        FieldEvidenceVariantAminoacidDescriptions,
    ],
)
