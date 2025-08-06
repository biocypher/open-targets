"""Acquisition definition that acquires nodes of text mining sentences."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceTextMiningSentences,
    FieldEvidenceTextMiningSentencesElementDEnd,
    FieldEvidenceTextMiningSentencesElementDStart,
    FieldEvidenceTextMiningSentencesElementSection,
    FieldEvidenceTextMiningSentencesElementTEnd,
    FieldEvidenceTextMiningSentencesElementText,
    FieldEvidenceTextMiningSentencesElementTStart,
)

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
        FieldEvidenceTextMiningSentencesElementDEnd,
        FieldEvidenceTextMiningSentencesElementDStart,
        FieldEvidenceTextMiningSentencesElementSection,
        FieldEvidenceTextMiningSentencesElementTEnd,
        FieldEvidenceTextMiningSentencesElementTStart,
        FieldEvidenceTextMiningSentencesElementText,
    ],
)
