"""Summary: CREDIBLE_SET nodes from CredibleSet dataset.

Definition for CREDIBLE_SET nodes: represents a set of candidate variants (credible set)
fine-mapped from a StudyLocus, capturing method, confidence, and physical coordinates.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetCredibleSet,
    FieldCredibleSetBeta,
    FieldCredibleSetChromosome,
    FieldCredibleSetConfidence,
    FieldCredibleSetCredibleSetIndex,
    FieldCredibleSetCredibleSetlog10Bf,
    FieldCredibleSetFinemappingMethod,
    FieldCredibleSetLocusEnd,
    FieldCredibleSetLocusStart,
    FieldCredibleSetPosition,
    FieldCredibleSetPurityMeanR2,
    FieldCredibleSetPurityMinR2,
    FieldCredibleSetPValueExponent,
    FieldCredibleSetPValueMantissa,
    FieldCredibleSetSampleSize,
    FieldCredibleSetStudyLocusId,
)

node_credible_set: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetCredibleSet),
    primary_id=FieldCredibleSetStudyLocusId,
    label="CREDIBLE_SET",
    properties=[
        FieldCredibleSetChromosome,
        FieldCredibleSetLocusStart,
        FieldCredibleSetLocusEnd,
        FieldCredibleSetPosition,
        FieldCredibleSetFinemappingMethod,
        FieldCredibleSetConfidence,
        FieldCredibleSetCredibleSetlog10Bf,
        FieldCredibleSetCredibleSetIndex,
        FieldCredibleSetSampleSize,
        FieldCredibleSetPurityMeanR2,
        FieldCredibleSetPurityMinR2,
        FieldCredibleSetPValueMantissa,
        FieldCredibleSetPValueExponent,
        FieldCredibleSetBeta,
    ],
)
