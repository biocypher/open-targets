"""Acquisition definition that acquires edges from targets to keywords."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetSearchTarget,
    FieldSearchTargetId,
    FieldSearchTargetKeywords,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_keyword: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetSearchTarget,
        exploded_field=FieldSearchTargetKeywords,
    ),
    primary_id=get_arrow_expression(FieldSearchTargetId, FieldSearchTargetKeywords.element),
    source=FieldSearchTargetId,
    target=FieldSearchTargetKeywords.element,
    label="HAS_KEYWORD",
    properties=[],
)
