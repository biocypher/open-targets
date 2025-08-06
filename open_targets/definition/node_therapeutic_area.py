"""Acquisition definition that acquires nodes of therapeutic areas."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesTherapeuticAreas,
    FieldDiseasesTherapeuticAreasElement,
)

node_therapeutic_area: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesTherapeuticAreas,
    ),
    primary_id=FieldDiseasesTherapeuticAreasElement,
    label="THERAPEUTIC_AREA",
    properties=[],
)
