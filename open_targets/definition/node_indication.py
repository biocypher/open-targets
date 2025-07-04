"""Acquisition definition that acquires nodes of indications."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetIndication,
    FieldIndicationId,
    FieldIndicationIndications,
    FieldIndicationIndicationsElementDisease,
    FieldIndicationIndicationsElementEfoName,
    FieldIndicationIndicationsElementMaxPhaseForIndication,
)
from open_targets.definition.helper import get_arrow_expression

node_indication: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetIndication,
        exploded_field=FieldIndicationIndications,
    ),
    primary_id=get_arrow_expression(FieldIndicationId, FieldIndicationIndicationsElementDisease),
    label="INDICATION",
    properties=[
        FieldIndicationIndicationsElementEfoName,
        FieldIndicationIndicationsElementMaxPhaseForIndication,
    ],
)
