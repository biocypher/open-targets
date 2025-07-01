"""Acquisition definition that acquires edges from evidence to text mining sentences."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceTextMiningSentences,
    FieldEvidenceTextMiningSentencesElementText,
)
from open_targets.definition.helper import get_arrow_expression
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression

edge_evidence_has_text_mining_sentence: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceTextMiningSentences,
    ),
    primary_id=get_arrow_expression(
        FieldEvidenceId,
        BuildCurieExpression(
            prefix=LiteralExpression("text_mining_sentence"),
            reference=FieldExpression(FieldEvidenceTextMiningSentencesElementText),
        ),
    ),
    source=FieldEvidenceId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("text_mining_sentence"),
        reference=FieldExpression(FieldEvidenceTextMiningSentencesElementText),
    ),
    label="HAS_TEXT_MINING_SENTENCE",
    properties=[],
)
