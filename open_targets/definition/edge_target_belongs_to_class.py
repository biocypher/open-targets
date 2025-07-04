"""Acquisition definition that acquires edges from targets to target classes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsTargetClass,
    FieldTargetsTargetClassElementId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_belongs_to_class: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsTargetClass,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsTargetClassElementId),
    source=FieldTargetsId,
    target=FieldTargetsTargetClassElementId,
    label="BELONGS_TO_CLASS",
    properties=[],
)