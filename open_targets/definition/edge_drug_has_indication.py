"""Acquisition definition that acquires 'has indication' edges for drugs."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetIndication,
    FieldIndicationId,
    FieldIndicationIndications,
    FieldIndicationIndicationsElementDisease,
)
from open_targets.definition.helper import get_arrow_expression

edge_drug_has_indication: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetIndication,
        exploded_field=FieldIndicationIndications,
    ),
    primary_id=get_arrow_expression(
        FieldIndicationId,
        get_arrow_expression(FieldIndicationId, FieldIndicationIndicationsElementDisease),
    ),
    source=FieldIndicationId,
    target=get_arrow_expression(FieldIndicationId, FieldIndicationIndicationsElementDisease),
    label="HAS_INDICATION",
    properties=[],
)
