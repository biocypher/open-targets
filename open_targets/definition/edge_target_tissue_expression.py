"""Acquisition definition that acquires edges between targets and tissues based on expression data."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetBaselineExpression,
    FieldBaselineExpressionId,
    FieldBaselineExpressionTissues,
    FieldBaselineExpressionTissuesElementEfoCode,
    FieldBaselineExpressionTissuesElementProtein,
    FieldBaselineExpressionTissuesElementRna,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_tissue_expression: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetBaselineExpression,
        exploded_field=FieldBaselineExpressionTissues,
    ),
    primary_id=get_arrow_expression(FieldBaselineExpressionId, FieldBaselineExpressionTissuesElementEfoCode),
    source=FieldBaselineExpressionId,
    target=FieldBaselineExpressionTissuesElementEfoCode,
    label="TARGET_TISSUE_EXPRESSION",
    properties=[
        FieldBaselineExpressionTissuesElementRnaValue,
        FieldBaselineExpressionTissuesElementRnaZscore,
        FieldBaselineExpressionTissuesElementRnaLevel,
        FieldBaselineExpressionTissuesElementRnaUnit,
        FieldBaselineExpressionTissuesElementProteinReliability,
        FieldBaselineExpressionTissuesElementProteinLevel,
    ],
)
