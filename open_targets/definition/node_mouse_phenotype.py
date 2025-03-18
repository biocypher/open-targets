"""Generation definitions for nodes of mouse phenotypes."""

from typing import Final

from open_targets.adapter.expression import ExtractCurieSchemeExpression, FieldExpression, NormaliseCurieExpression
from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesModelPhenotypeId,
    FieldMousePhenotypesModelPhenotypeLabel,
)
from open_targets.definition.node_shared import node_static_properties

node_mouse_phenotype: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=NormaliseCurieExpression(FieldExpression(FieldMousePhenotypesModelPhenotypeId)),
    label=ExtractCurieSchemeExpression(FieldExpression(FieldMousePhenotypesModelPhenotypeId)),
    properties=[
        FieldMousePhenotypesModelPhenotypeLabel,
        *node_static_properties,
    ],
)
