"""Generation definition for edges between targets and diseases."""

from typing import Final

from open_targets.adapter.expression import (
    BuildCurieExpression,
    DataSourceToLicenceExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
)
from open_targets.adapter.generation_definition import ExpressionEdgeGenerationDefinition, GenerationDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDatatypeId,
    FieldEvidenceDiseaseId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetId,
)

edge_target_disease: Final[GenerationDefinition[EdgeInfo]] = ExpressionEdgeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceId,
    source=BuildCurieExpression(
        scheme=LiteralExpression("ensembl"),
        path=FieldExpression(FieldEvidenceTargetId),
        normalised=True,
    ),
    target=NormaliseCurieExpression(FieldExpression(FieldEvidenceDiseaseId)),
    label=FieldEvidenceDatatypeId,
    properties=[
        FieldEvidenceDatasourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        ("source", FieldEvidenceDatasourceId),
        ("licence", DataSourceToLicenceExpression(FieldExpression(FieldEvidenceDatasourceId))),
    ],
)
