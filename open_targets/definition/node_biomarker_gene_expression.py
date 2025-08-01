"""Acquisition definition that acquires nodes of gene expression biomarkers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiomarkersGeneExpression,
    FieldEvidenceBiomarkersGeneExpressionElementId,
    FieldEvidenceBiomarkersGeneExpressionElementName,
)

node_biomarker_gene_expression: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceBiomarkersGeneExpression,
    ),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression("gene_expression"),
        reference=FieldExpression(FieldEvidenceBiomarkersGeneExpressionElementId),
    ),
    label="BIOMARKER",
    properties=[
        FieldEvidenceBiomarkersGeneExpressionElementName,
    ],
)
