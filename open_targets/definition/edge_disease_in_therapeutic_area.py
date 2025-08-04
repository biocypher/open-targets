"""Acquisition definition that acquires 'is in therapeutic area' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesTherapeuticAreas,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_in_therapeutic_area: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesTherapeuticAreas,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesTherapeuticAreasElement),
    source=FieldDiseasesId,
    target=FieldDiseasesTherapeuticAreasElement,
    label="IS_IN_THERAPEUTIC_AREA",
    properties=[],
)
