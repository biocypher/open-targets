"""Acquisition definition that acquires nodes of mechanisms of action."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMechanismOfAction,
    FieldMechanismOfActionActionType,
    FieldMechanismOfActionChemblIds,
    FieldMechanismOfActionChemblIdsElement,
    FieldMechanismOfActionMechanismOfAction,
    FieldMechanismOfActionTargetName,
    FieldMechanismOfActionTargetType,
)
from open_targets.definition.helper import get_arrow_expression

node_mechanism_of_action: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMechanismOfAction,
        exploded_field=FieldMechanismOfActionChemblIds,
    ),
    primary_id=get_arrow_expression(FieldMechanismOfActionChemblIdsElement, FieldMechanismOfActionMechanismOfAction),
    label="MECHANISM_OF_ACTION",
    properties=[
        FieldMechanismOfActionActionType,
        FieldMechanismOfActionMechanismOfAction,
        FieldMechanismOfActionTargetName,
        FieldMechanismOfActionTargetType,
    ],
)
