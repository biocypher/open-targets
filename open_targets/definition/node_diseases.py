"""Generation definitions for nodes of diseases."""

from typing import Final

from open_targets.adapter.expression import (
    ExtractCuriePrefixExpression,
    FieldExpression,
    NormaliseCurieExpression,
)
from open_targets.adapter.generation_definition import ExpressionNodeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesCode,
    FieldDiseasesDescription,
    FieldDiseasesId,
    FieldDiseasesName,
)
from open_targets.definition.node_shared import node_static_properties

node_diseases: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetDiseases),
    primary_id=NormaliseCurieExpression(expression=FieldExpression(FieldDiseasesId)),
    label=ExtractCuriePrefixExpression(FieldExpression(FieldDiseasesId)),
    properties=[
        FieldDiseasesCode,
        FieldDiseasesDescription,
        FieldDiseasesName,
        *node_static_properties,
    ],
)
