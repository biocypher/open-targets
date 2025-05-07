"""Acquisition definition that acquires nodes of GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import (
    ExtractCuriePrefixExpression,
    FieldExpression,
    NormaliseCurieExpression,
    ToStringExpression,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetGo,
    FieldGoId,
    FieldGoName,
)
from open_targets.definition.node_shared import node_static_properties

node_gene_ontology: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetGo),
    primary_id=NormaliseCurieExpression(expression=ToStringExpression(FieldExpression(FieldGoId))),
    label=ExtractCuriePrefixExpression(expression=ToStringExpression(FieldExpression(FieldGoId))),
    properties=[
        FieldGoName,
        *node_static_properties,
    ],
)
