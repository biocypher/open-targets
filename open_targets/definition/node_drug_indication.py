"""Acquisition definition that acquires nodes of drug indications."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetKnownDrugsAggregated,
    FieldKnownDrugsAggregatedApprovedName,
    FieldKnownDrugsAggregatedApprovedSymbol,
    FieldKnownDrugsAggregatedDiseaseId,
    FieldKnownDrugsAggregatedDrugId,
    FieldKnownDrugsAggregatedDrugType,
    FieldKnownDrugsAggregatedLabel,
    FieldKnownDrugsAggregatedMechanismOfAction,
    FieldKnownDrugsAggregatedPhase,
    FieldKnownDrugsAggregatedPrefName,
    FieldKnownDrugsAggregatedStatus,
    FieldKnownDrugsAggregatedTargetClass,
    FieldKnownDrugsAggregatedTargetId,
    FieldKnownDrugsAggregatedTargetName,
)
from open_targets.definition.helper import get_arrow_expression

node_drug_indication: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetKnownDrugsAggregated),
    primary_id=get_arrow_expression(FieldKnownDrugsAggregatedDrugId, FieldKnownDrugsAggregatedDiseaseId),
    label="DRUG_INDICATION",
    properties=[
        FieldKnownDrugsAggregatedApprovedName,
        FieldKnownDrugsAggregatedApprovedSymbol,
        FieldKnownDrugsAggregatedDrugType,
        FieldKnownDrugsAggregatedLabel,
        FieldKnownDrugsAggregatedMechanismOfAction,
        FieldKnownDrugsAggregatedPhase,
        FieldKnownDrugsAggregatedPrefName,
        FieldKnownDrugsAggregatedStatus,
        FieldKnownDrugsAggregatedTargetClass,
        FieldKnownDrugsAggregatedTargetId,
        FieldKnownDrugsAggregatedTargetName,
    ],
)
