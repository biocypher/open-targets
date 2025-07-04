"""Acquisition definition that acquires edges from targets to TEP information."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsTepTargetFromSourceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_tep_info: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargets),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsTepTargetFromSourceId),
    source=FieldTargetsId,
    target=FieldTargetsTepTargetFromSourceId,
    label="HAS_TEP_INFO",
    properties=[],
)