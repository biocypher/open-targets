"""Acquisition definition for edges between targets and diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    DataSourceToLicenceExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    ToStringExpression,
)
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
from open_targets.definition.curie_prefix import ENSEMBL_PREFIX

edge_target_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceId,
    source=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldEvidenceTargetId),
        normalise=True,
    ),
    target=NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldEvidenceDiseaseId))),
    label=FieldEvidenceDatatypeId,
    properties=[
        FieldEvidenceDatasourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        ("source", FieldEvidenceDatasourceId),
        ("licence", DataSourceToLicenceExpression(ToStringExpression(FieldExpression(FieldEvidenceDatasourceId)))),
    ],
)
