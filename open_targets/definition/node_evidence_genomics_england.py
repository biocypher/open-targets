"""Acquisition definition that acquires nodes of Genomics England evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceAllelicRequirements,
    FieldEvidenceCohortPhenotypes,
    FieldEvidenceConfidence,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceStudyId,
    FieldEvidenceStudyOverview,
)

node_evidence_genomics_england: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'genomics_england'",
    ),
    primary_id=FieldEvidenceId,
    label="GENOMICS_ENGLAND_EVIDENCE",
    properties=[
        FieldEvidenceAllelicRequirements,
        FieldEvidenceCohortPhenotypes,
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceStudyId,
        FieldEvidenceStudyOverview,
    ],
)
