"""Acquisition definition that acquires nodes of species A."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetInteraction,
    FieldInteractionSpeciesAScientificName,
    FieldInteractionSpeciesATaxonId,
)

node_species_a: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetInteraction),
    primary_id=FieldInteractionSpeciesATaxonId,
    label="SPECIES",
    properties=[
        FieldInteractionSpeciesAScientificName,
    ],
)
