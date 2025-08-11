"""Acquisition definition that acquires nodes of UniProt variants evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceConfidence,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetModulation,
    FieldEvidenceVariantFunctionalConsequenceId,
    FieldEvidenceVariantId,
    FieldEvidenceVariantRsId,
)

node_evidence_uniprot_variants: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'uniprot_variants'",
    ),
    primary_id=FieldEvidenceId,
    label="UNIPROT_VARIANTS_EVIDENCE",
    properties=[
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceTargetModulation,
        FieldEvidenceVariantFunctionalConsequenceId,
        FieldEvidenceVariantId,
        FieldEvidenceVariantRsId,
    ],
)
