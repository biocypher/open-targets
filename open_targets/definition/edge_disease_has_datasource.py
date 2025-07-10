"""Acquisition definition that acquires edges from diseases to datasources."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetFacetSearchDisease,
    FieldFacetSearchDiseaseEntityIds,
    FieldFacetSearchDiseaseDatasourceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_datasource: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetFacetSearchDisease,
        exploded_field=FieldFacetSearchDiseaseEntityIds,
    ),
    primary_id=get_arrow_expression(FieldFacetSearchDiseaseEntityIds.element, FieldFacetSearchDiseaseDatasourceId),
    source=FieldFacetSearchDiseaseEntityIds.element,
    target=FieldFacetSearchDiseaseDatasourceId,
    label="HAS_DATASOURCE",
    properties=[],
)
