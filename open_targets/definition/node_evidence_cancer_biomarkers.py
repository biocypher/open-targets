"""Acquisition definition that acquires nodes of Cancer Biomarkers evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceBiomarkerName,
    FieldEvidenceBiomarkers,
    FieldEvidenceConfidence,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDrugFromSource,
    FieldEvidenceDrugId,
    FieldEvidenceDrugResponse,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceUrls,
)

node_evidence_cancer_biomarkers: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'cancer_biomarkers'",
    ),
    primary_id=FieldEvidenceId,
    label="CANCER_BIOMARKERS_EVIDENCE",
    properties=[
        FieldEvidenceBiomarkerName,
        FieldEvidenceBiomarkers,
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDrugFromSource,
        FieldEvidenceDrugId,
        FieldEvidenceDrugResponse,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceUrls,
    ],
)
