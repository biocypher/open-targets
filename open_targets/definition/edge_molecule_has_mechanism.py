"""Acquisition definition that acquires 'has mechanism' edges for molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMechanismOfAction,
    FieldMechanismOfActionChemblIds,
    FieldMechanismOfActionChemblIdsElement,
    FieldMechanismOfActionMechanismOfAction,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_has_mechanism: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMechanismOfAction,
        exploded_field=FieldMechanismOfActionChemblIds,
    ),
    primary_id=get_arrow_expression(
        FieldMechanismOfActionChemblIdsElement,
        get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
    ),
    source=FieldMechanismOfActionChemblIdsElement,
    target=get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
    label="HAS_MECHANISM",
    properties=[],
)
