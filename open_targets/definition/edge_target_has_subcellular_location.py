"""Acquisition definition that acquires edges from targets to subcellular locations."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsSubcellularLocations,
    FieldTargetsSubcellularLocationsElementLocation,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_subcellular_location: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsSubcellularLocations,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsSubcellularLocationsElementLocation),
    source=FieldTargetsId,
    target=FieldTargetsSubcellularLocationsElementLocation,
    label="HAS_SUBCELLULAR_LOCATION",
    properties=[],
)