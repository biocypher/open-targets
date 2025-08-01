"""Acquisition definition that acquires 'in species A' edges for interactions."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetInteraction,
    FieldInteractionSpeciesATaxonId,
    FieldInteractionTargetA,
    FieldInteractionTargetB,
)
from open_targets.definition.helper import get_arrow_expression

edge_interaction_in_species_a: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetInteraction),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldInteractionTargetA, FieldInteractionTargetB),
        FieldInteractionSpeciesATaxonId,
    ),
    source=get_arrow_expression(FieldInteractionTargetA, FieldInteractionTargetB),
    target=FieldInteractionSpeciesATaxonId,
    label="INTERACTS_IN_SPECIES",
    properties=[],
)
