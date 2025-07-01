"""Acquisition definition that acquires 'is a' edges between diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesParents,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_is_a: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesParents,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesParents.element),
    source=FieldDiseasesId,
    target=FieldDiseasesParents.element,
    label="DISEASE_IS_A",
    properties=[],
)
