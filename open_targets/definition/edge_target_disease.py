from typing import Final

from open_targets.adapter.generation_definition import GenerationDefinition, SimpleEdgeGenerationDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.data.schema import (
    FieldEvidenceDatasourceId,
    FieldEvidenceDatatypeId,
    FieldEvidenceDiseaseId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetId,
)

edge_target_disease: Final[GenerationDefinition[EdgeInfo]] = SimpleEdgeGenerationDefinition(
    primary_id=FieldEvidenceId,
    source=FieldEvidenceTargetId,
    target=FieldEvidenceDiseaseId,
    labels=[],
    properties=[
        FieldEvidenceDatatypeId,
        FieldEvidenceDatasourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
    ],
)
