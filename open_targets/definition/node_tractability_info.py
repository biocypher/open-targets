"""Acquisition definition that acquires nodes of tractability information."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsTractability,
    FieldTargetsTractabilityElementId,
    FieldTargetsTractabilityElementModality,
    FieldTargetsTractabilityElementValue,
)

node_tractability_info: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsTractability,
    ),
    primary_id=FieldTargetsTractabilityElementId,
    label="TRACTABILITY_INFO",
    properties=[
        FieldTargetsTractabilityElementModality,
        FieldTargetsTractabilityElementValue,
    ],
)