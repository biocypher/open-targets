"""Acquisition definition that acquires edges from targets to cross-references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsDbXrefs,
    FieldTargetsDbXrefsElementId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_xref: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsDbXrefs,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsDbXrefsElementId),
    source=FieldTargetsId,
    target=FieldTargetsDbXrefsElementId,
    label="TARGET_HAS_XREF",
    properties=[],
)
