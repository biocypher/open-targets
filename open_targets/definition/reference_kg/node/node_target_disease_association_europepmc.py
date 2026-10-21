"""Summary: text-mined literature co-mentions (Europe PMC).

Definition for TARGET_DISEASE_ASSOCIATION_EUROPEPMC nodes: filters Evidence
parquet to europepmc text-mined literature evidence. Co-mentions of targets and
diseases in publications are scored (resource score/overall score) and mapped to
target/disease IDs. Inference: mine papers → detect target–disease co-mention →
assign relevance score → represent as literature-derived association in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import FieldExpression, TransformExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceEuropepmc,
    FieldEvidenceEuropepmcDiseaseFromSourceMappedId,
    FieldEvidenceEuropepmcId,
    FieldEvidenceEuropepmcLiterature,
    FieldEvidenceEuropepmcResourceScore,
    FieldEvidenceEuropepmcScore,
    FieldEvidenceEuropepmcTargetFromSourceId,
    FieldEvidenceEuropepmcTextMiningSentences,
    FieldEvidenceEuropepmcTextMiningSentencesElementText,
)

node_target_disease_association_europepmc: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidenceEuropepmc),
    primary_id=FieldEvidenceEuropepmcId,
    label="TARGET_DISEASE_ASSOCIATION_EUROPEPMC",
    properties=[
        FieldEvidenceEuropepmcDiseaseFromSourceMappedId,
        FieldEvidenceEuropepmcLiterature,
        FieldEvidenceEuropepmcResourceScore,
        FieldEvidenceEuropepmcScore,
        FieldEvidenceEuropepmcTargetFromSourceId,
        (
            FieldEvidenceEuropepmcTextMiningSentences.name,
            TransformExpression(
                FieldExpression(FieldEvidenceEuropepmcTextMiningSentences),
                lambda sentences: [
                    str(sentence[FieldEvidenceEuropepmcTextMiningSentencesElementText])
                    for sentence in sentences
                    if sentence[FieldEvidenceEuropepmcTextMiningSentencesElementText] is not None
                ],
            ),
        ),
    ],
)
