"""Acquisition definition that acquires edges from mechanisms of action to references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMechanismOfAction,
    FieldMechanismOfActionMechanismOfAction,
    FieldMechanismOfActionReferences,
)
from open_targets.definition.helper import get_arrow_expression

edge_mechanism_has_reference: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMechanismOfAction,
        exploded_field=FieldMechanismOfActionReferences,
    ),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
        FieldMechanismOfActionReferencesElementIdsElement,
    ),
    source=get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
    target=FieldMechanismOfActionReferencesElementIdsElement,
    label="HAS_REFERENCE",
    properties=[],
)
