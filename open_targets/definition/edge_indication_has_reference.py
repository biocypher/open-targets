"""Acquisition definition that acquires edges from indications to references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetIndication,
    FieldIndicationId,
    FieldIndicationIndicationsElementDisease,
    FieldIndicationIndicationsElementReferences,
    FieldIndicationIndicationsElementReferencesElementIdsElement,
)
from open_targets.definition.helper import get_arrow_expression

edge_indication_has_reference: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetIndication,
        exploded_field=FieldIndicationIndicationsElementReferences,
    ),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldIndicationId, FieldIndicationIndicationsElementDisease),
        FieldIndicationIndicationsElementReferencesElementIdsElement,
    ),
    source=get_arrow_expression(FieldIndicationId, FieldIndicationIndicationsElementDisease),
    target=FieldIndicationIndicationsElementReferencesElementIdsElement,
    label="HAS_REFERENCE",
    properties=[],
)
