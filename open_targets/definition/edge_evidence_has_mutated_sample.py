"""Acquisition definition that acquires edges from evidence to mutated samples."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceMutatedSamples,
    FieldEvidenceMutatedSamplesElementFunctionalConsequenceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_mutated_sample: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceMutatedSamples,
    ),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceMutatedSamplesElementFunctionalConsequenceId),
    source=FieldEvidenceId,
    target=FieldEvidenceMutatedSamplesElementFunctionalConsequenceId,
    label="HAS_MUTATED_SAMPLE",
    properties=[],
)
