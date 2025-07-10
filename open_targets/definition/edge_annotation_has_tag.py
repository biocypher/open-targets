"""Acquisition definition that acquires edges from annotations to tags."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.expression import FieldExpression
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementTags,
    FieldEpmcCooccurrencesAnnsElementTagsElementName,
    FieldEpmcCooccurrencesAnnsElementExact,
)
from open_targets.definition.helper import get_arrow_expression

edge_annotation_has_tag: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnnsElementTags,
    ),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldEpmcCooccurrencesAnns.element, FieldEpmcCooccurrencesAnnsElementExact),
        FieldEpmcCooccurrencesAnnsElementTagsElementName,
    ),
    source=get_arrow_expression(FieldEpmcCooccurrencesAnns.element, FieldEpmcCooccurrencesAnnsElementExact),
    target=FieldEpmcCooccurrencesAnnsElementTagsElementName,
    label="HAS_TAG",
    properties=[],
)
