"""Acquisition definition that acquires nodes of categories."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetFacetSearchDisease,
    FieldFacetSearchDiseaseCategory,
)

node_category: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetFacetSearchDisease,
        exploded_field=FieldFacetSearchDiseaseCategory,
    ),
    primary_id=FieldFacetSearchDiseaseCategory.element,
    label="CATEGORY",
    properties=[],
)
