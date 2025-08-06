"""Acquisition definition that acquires edges from evidence to pubmed literature entries."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceLiteratureElement,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_literature_pubmed: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceLiterature,
    ),
    primary_id=get_arrow_expression(
        FieldEvidenceId,
        BuildCurieExpression(
            prefix=LiteralExpression("pubmed"),
            reference=FieldExpression(FieldEvidenceLiteratureElement),
        ),
    ),
    source=FieldEvidenceId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("pubmed"),
        reference=FieldExpression(FieldEvidenceLiteratureElement),
    ),
    label="HAS_LITERATURE",
    properties=[],
)
