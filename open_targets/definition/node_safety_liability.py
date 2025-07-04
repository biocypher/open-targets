"""Acquisition definition that acquires nodes of safety liabilities."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsSafetyLiabilities,
    FieldTargetsSafetyLiabilitiesElementEventId,
    FieldTargetsSafetyLiabilitiesElementDatasource,
    FieldTargetsSafetyLiabilitiesElementEvent,
    FieldTargetsSafetyLiabilitiesElementLiterature,
    FieldTargetsSafetyLiabilitiesElementUrl,
)

node_safety_liability: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsSafetyLiabilities,
    ),
    primary_id=FieldTargetsSafetyLiabilitiesElementEventId,
    label="SAFETY_LIABILITY",
    properties=[
        FieldTargetsSafetyLiabilitiesElementDatasource,
        FieldTargetsSafetyLiabilitiesElementEvent,
        FieldTargetsSafetyLiabilitiesElementLiterature,
        FieldTargetsSafetyLiabilitiesElementUrl,
    ],
)
