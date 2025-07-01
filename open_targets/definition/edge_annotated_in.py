"""Acquisition definition that acquires edges between annotations and publications."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementExact,
    FieldEpmcCooccurrencesId,
)
from open_targets.definition.helper import get_arrow_expression

edge_annotated_in: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnns,
    ),
    primary_id=get_arrow_expression(
        BuildCurieExpression(
            prefix=FieldExpression(FieldEpmcCooccurrencesId),
            reference=FieldExpression(FieldEpmcCooccurrencesAnnsElementExact),
        ),
        FieldEpmcCooccurrencesId,
    ),
    source=BuildCurieExpression(
        prefix=FieldExpression(FieldEpmcCooccurrencesId),
        reference=FieldExpression(FieldEpmcCooccurrencesAnnsElementExact),
    ),
    target=FieldEpmcCooccurrencesId,
    label="ANNOTATED_IN",
    properties=[],
)
