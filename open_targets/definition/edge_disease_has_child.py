"""Acquisition definition that acquires 'has child' edges between diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesChildren,
    FieldDiseasesId,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_child: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesChildren,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesChildrenElement),
    source=FieldDiseasesId,
    target=FieldDiseasesChildrenElement,
    label="DISEASE_HAS_CHILD",
    properties=[],
)
