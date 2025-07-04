"""Acquisition definition that acquires edges from targets to hallmarks."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsHallmarks,
    FieldTargetsHallmarksCancerHallmarks,
    FieldTargetsHallmarksCancerHallmarksElementLabel,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_hallmark: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsHallmarksCancerHallmarks,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsHallmarksCancerHallmarksElementLabel),
    source=FieldTargetsId,
    target=FieldTargetsHallmarksCancerHallmarksElementLabel,
    label="HAS_HALLMARK",
    properties=[],
)
