"""Acquisition definition that acquires nodes of text mining sentences."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceTextMiningSentences,
    FieldEvidenceTextMiningSentencesElementDend,
    FieldEvidenceTextMiningSentencesElementDstart,
    FieldEvidenceTextMiningSentencesElementSection,
    FieldEvidenceTextMiningSentencesElementTend,
    FieldEvidenceTextMiningSentencesElementTstart,
    FieldEvidenceTextMiningSentencesElementText,
)
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression

node_text_mining_sentence: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceTextMiningSentences,
    ),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression("text_mining_sentence"),
        reference=FieldExpression(FieldEvidenceTextMiningSentencesElementText),
    ),
    label="TEXT_MINING_SENTENCE",
    properties=[
        FieldEvidenceTextMiningSentencesElementDend,
        FieldEvidenceTextMiningSentencesElementDstart,
        FieldEvidenceTextMiningSentencesElementSection,
        FieldEvidenceTextMiningSentencesElementTend,
        FieldEvidenceTextMiningSentencesElementTstart,
        FieldEvidenceTextMiningSentencesElementText,
    ],
)
