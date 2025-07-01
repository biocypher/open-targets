"""Acquisition definition that acquires nodes of variants."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceVariantId,
    FieldEvidenceVariantAminoacidDescriptions,
    FieldEvidenceVariantEffect,
    FieldEvidenceVariantFunctionalConsequenceFromQtlId,
    FieldEvidenceVariantFunctionalConsequenceId,
    FieldEvidenceVariantHgvsId,
    FieldEvidenceVariantRsId,
)

node_variant: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceVariantId,
    label="VARIANT",
    properties=[
        FieldEvidenceVariantAminoacidDescriptions,
        FieldEvidenceVariantEffect,
        FieldEvidenceVariantFunctionalConsequenceFromQtlId,
        FieldEvidenceVariantFunctionalConsequenceId,
        FieldEvidenceVariantHgvsId,
        FieldEvidenceVariantRsId,
    ],
)
