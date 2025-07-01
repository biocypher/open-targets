"""Acquisition definition that acquires nodes of tissues."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetBaselineExpression,
    FieldBaselineExpressionTissues,
    FieldBaselineExpressionTissuesElementEfoCode,
    FieldBaselineExpressionTissuesElementLabel,
)

node_tissue: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetBaselineExpression,
        exploded_field=FieldBaselineExpressionTissues,
    ),
    primary_id=FieldBaselineExpressionTissuesElementEfoCode,
    label="TISSUE",
    properties=[
        FieldBaselineExpressionTissuesElementLabel,
        FieldBaselineExpressionTissuesElementAnatomicalSystems,
        FieldBaselineExpressionTissuesElementOrgans,
    ],
)
