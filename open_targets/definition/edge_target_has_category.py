"""Acquisition definition that acquires edges from targets to categories."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetFacetSearchTarget,
    FieldFacetSearchTargetEntityIds,
    FieldFacetSearchTargetCategory,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_category: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetFacetSearchTarget,
        exploded_field=FieldFacetSearchTargetCategory,
    ),
    primary_id=get_arrow_expression(FieldFacetSearchTargetEntityIds.element, FieldFacetSearchTargetCategory.element),
    source=FieldFacetSearchTargetEntityIds.element,
    target=FieldFacetSearchTargetCategory.element,
    label="HAS_CATEGORY",
    properties=[],
)
