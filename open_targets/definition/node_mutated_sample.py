"""Acquisition definition that acquires nodes of mutated samples."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceMutatedSamples,
    FieldEvidenceMutatedSamplesElementFunctionalConsequenceId,
    FieldEvidenceMutatedSamplesElementNumberMutatedSamples,
    FieldEvidenceMutatedSamplesElementNumberSamplesTested,
    FieldEvidenceMutatedSamplesElementNumberSamplesWithMutationType,
)

node_mutated_sample: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceMutatedSamples,
    ),
    primary_id=FieldEvidenceMutatedSamplesElementFunctionalConsequenceId,
    label="MUTATED_SAMPLE",
    properties=[
        FieldEvidenceMutatedSamplesElementNumberMutatedSamples,
        FieldEvidenceMutatedSamplesElementNumberSamplesTested,
        FieldEvidenceMutatedSamplesElementNumberSamplesWithMutationType,
    ],
)
