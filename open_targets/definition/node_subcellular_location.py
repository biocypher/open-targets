"""Acquisition definition that acquires nodes of subcellular locations."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsSubcellularLocations,
    FieldTargetsSubcellularLocationsElementLabelSl,
    FieldTargetsSubcellularLocationsElementLocation,
    FieldTargetsSubcellularLocationsElementSource,
    FieldTargetsSubcellularLocationsElementTermSl,
)

node_subcellular_location: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsSubcellularLocations,
    ),
    primary_id=FieldTargetsSubcellularLocationsElementLocation,
    label="SUBCELLULAR_LOCATION",
    properties=[
        FieldTargetsSubcellularLocationsElementLabelSl,
        FieldTargetsSubcellularLocationsElementSource,
        FieldTargetsSubcellularLocationsElementTermSl,
    ],
)
