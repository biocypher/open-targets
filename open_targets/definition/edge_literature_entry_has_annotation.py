"""Acquisition definition that acquires edges from literature entries to annotations."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.expression import FieldExpression
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesId,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementExact,
)
from open_targets.definition.helper import get_arrow_expression

edge_literature_entry_has_annotation: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnns,
    ),
    primary_id=get_arrow_expression(FieldEpmcCooccurrencesId, FieldEpmcCooccurrencesAnnsElementExact),
    source=FieldEpmcCooccurrencesId,
    target=FieldEpmcCooccurrencesAnnsElementExact,
    label="HAS_ANNOTATION",
    properties=[],
)
