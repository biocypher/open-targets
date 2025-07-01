"""Acquisition definition that acquires nodes of targets."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsApprovedSymbol,
    FieldTargetsBiotype,
    FieldTargetsId,
)

node_targets: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargets),
    primary_id=FieldTargetsId,
    label="TARGET",
    properties=[
        FieldTargetsApprovedSymbol,
        FieldTargetsBiotype,
    ],
)
