"""Acquisition definition that acquires nodes of target classes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsTargetClass,
    FieldTargetsTargetClassElementId,
    FieldTargetsTargetClassElementLabel,
    FieldTargetsTargetClassElementLevel,
)

node_target_class: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsTargetClass,
    ),
    primary_id=FieldTargetsTargetClassElementId,
    label="TARGET_CLASS",
    properties=[
        FieldTargetsTargetClassElementLabel,
        FieldTargetsTargetClassElementLevel,
    ],
)