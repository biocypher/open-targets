"""Acquisition definition that acquires edges from diseases to categories."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetFacetSearchDisease,
    FieldFacetSearchDiseaseEntityIds,
    FieldFacetSearchDiseaseCategory,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_category: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetFacetSearchDisease,
        exploded_field=FieldFacetSearchDiseaseCategory,
    ),
    primary_id=get_arrow_expression(FieldFacetSearchDiseaseEntityIds.element, FieldFacetSearchDiseaseCategory.element),
    source=FieldFacetSearchDiseaseEntityIds.element,
    target=FieldFacetSearchDiseaseCategory.element,
    label="HAS_CATEGORY",
    properties=[],
)
