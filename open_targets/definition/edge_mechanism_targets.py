"""Acquisition definition that acquires 'targets' edges from mechanisms of action to targets."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMechanismOfAction,
    FieldMechanismOfActionChemblIdsElement,
    FieldMechanismOfActionMechanismOfAction,
    FieldMechanismOfActionTargets,
    FieldMechanismOfActionTargetsElement,
)
from open_targets.definition.helper import get_arrow_expression

edge_mechanism_targets: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMechanismOfAction,
        exploded_field=FieldMechanismOfActionTargets,
    ),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
        FieldMechanismOfActionTargetsElement,
    ),
    source=get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
    target=FieldMechanismOfActionTargetsElement,
    label="MECHANISM_TARGETS",
    properties=[],
)
