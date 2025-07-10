"""Acquisition definition that acquires edges from targets to datasources."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetFacetSearchTarget,
    FieldFacetSearchTargetEntityIds,
    FieldFacetSearchTargetDatasourceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_datasource: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetFacetSearchTarget,
        exploded_field=FieldFacetSearchTargetEntityIds,
    ),
    primary_id=get_arrow_expression(FieldFacetSearchTargetEntityIds.element, FieldFacetSearchTargetDatasourceId),
    source=FieldFacetSearchTargetEntityIds.element,
    target=FieldFacetSearchTargetDatasourceId,
    label="HAS_DATASOURCE",
    properties=[],
)
