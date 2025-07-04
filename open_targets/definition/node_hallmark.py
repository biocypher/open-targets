"""Acquisition definition that acquires nodes of hallmarks."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsHallmarks,
    FieldTargetsHallmarksCancerHallmarks,
    FieldTargetsHallmarksCancerHallmarksElementLabel,
    FieldTargetsHallmarksCancerHallmarksElementDescription,
    FieldTargetsHallmarksCancerHallmarksElementImpact,
    FieldTargetsHallmarksCancerHallmarksElementPmid,
)

node_hallmark: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsHallmarksCancerHallmarks,
    ),
    primary_id=FieldTargetsHallmarksCancerHallmarksElementLabel,
    label="HALLMARK",
    properties=[
        FieldTargetsHallmarksCancerHallmarksElementDescription,
        FieldTargetsHallmarksCancerHallmarksElementImpact,
        FieldTargetsHallmarksCancerHallmarksElementPmid,
    ],
)
