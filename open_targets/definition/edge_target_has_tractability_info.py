"""Acquisition definition that acquires edges from targets to tractability information."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsTractability,
    FieldTargetsTractabilityElementId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_tractability_info: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsTractability,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsTractabilityElementId),
    source=FieldTargetsId,
    target=FieldTargetsTractabilityElementId,
    label="HAS_TRACTABILITY_INFO",
    properties=[],
)