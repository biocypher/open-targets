"""Acquisition definitions for nodes of mouse phenotypes."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.expression import (
    ExtractCuriePrefixExpression,
    FieldExpression,
    NormaliseCurieExpression,
    ToStringExpression,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesModelPhenotypeId,
    FieldMousePhenotypesModelPhenotypeLabel,
)
from open_targets.definition.node_shared import node_static_properties

node_mouse_phenotype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldMousePhenotypesModelPhenotypeId))),
    label=ExtractCuriePrefixExpression(ToStringExpression(FieldExpression(FieldMousePhenotypesModelPhenotypeId))),
    properties=[
        FieldMousePhenotypesModelPhenotypeLabel,
        *node_static_properties,
    ],
)
