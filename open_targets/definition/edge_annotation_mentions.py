"""Acquisition definition that acquires edges between annotations and mentioned entities."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementExact,
    FieldEpmcCooccurrencesAnnsElementTags,
    FieldEpmcCooccurrencesAnnsElementTagsElementUri,
    FieldEpmcCooccurrencesId,
)
from open_targets.definition.helper import get_arrow_expression

edge_annotation_mentions: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnns.element.f_tags,
    ),
    primary_id=get_arrow_expression(
        BuildCurieExpression(
            prefix=FieldExpression(FieldEpmcCooccurrencesId),
            reference=FieldExpression(FieldEpmcCooccurrencesAnns.element.f_exact),
        ),
        FieldEpmcCooccurrencesAnnsElementTagsElementUri,
    ),
    source=BuildCurieExpression(
        prefix=FieldExpression(FieldEpmcCooccurrencesId),
        reference=FieldExpression(FieldEpmcCooccurrencesAnns.element.f_exact),
    ),
    target=FieldEpmcCooccurrencesAnnsElementTagsElementUri,
    label="ANNOTATION_MENTIONS",
    properties=[],
)
