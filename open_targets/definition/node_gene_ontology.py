"""Generation definitions for nodes of GO terms."""

from typing import Final

from open_targets.adapter.expression import ExtractCurieSchemeExpression, FieldExpression, NormaliseCurieExpression
from open_targets.adapter.generation_definition import ExpressionNodeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetGo,
    FieldGoId,
    FieldGoName,
)
from open_targets.definition.node_shared import node_static_properties

node_gene_ontology: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetGo),
    primary_id=NormaliseCurieExpression(FieldExpression(FieldGoId)),
    label=ExtractCurieSchemeExpression(FieldExpression(FieldGoId)),
    properties=[
        FieldGoName,
        *node_static_properties,
    ],
)
