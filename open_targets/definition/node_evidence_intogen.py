"""Acquisition definition that acquires nodes of IntOGen evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceCohortDescription,
    FieldEvidenceCohortId,
    FieldEvidenceCohortShortName,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceId,
    FieldEvidenceMutatedSamples,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceSignificantDriverMethods,
    FieldEvidenceVariantEffect,
)

node_evidence_intogen: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        filter="datasourceId == 'intogen'",
    ),
    primary_id=FieldEvidenceId,
    label="INTOGEN_EVIDENCE",
    properties=[
        FieldEvidenceCohortDescription,
        FieldEvidenceCohortId,
        FieldEvidenceCohortShortName,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceMutatedSamples,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceSignificantDriverMethods,
        FieldEvidenceVariantEffect,
    ],
)
