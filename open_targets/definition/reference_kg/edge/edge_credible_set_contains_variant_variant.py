"""Summary: Edge connecting CREDIBLE_SET node to VARIANT node.

Definition for edge: CREDIBLE_SET -> VARIANT
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetCredibleSet,
    FieldCredibleSetLocus,
    FieldCredibleSetLocusElementBeta,
    FieldCredibleSetLocusElementLogBf,
    FieldCredibleSetLocusElementPosteriorProbability,
    FieldCredibleSetLocusElementPValueExponent,
    FieldCredibleSetLocusElementPValueMantissa,
    FieldCredibleSetLocusElementStandardError,
    FieldCredibleSetLocusElementVariantId,
    FieldCredibleSetStudyLocusId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_credible_set_contains_variant_variant: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetCredibleSet,
            exploded_field=FieldCredibleSetLocus,
        ),
        primary_id=NewUuidExpression(),
        source=FieldCredibleSetStudyLocusId,
        target=FieldCredibleSetLocusElementVariantId,
        label=EdgeLabel.CONTAINS_VARIANT,
        properties=[
            FieldCredibleSetLocusElementPosteriorProbability,
            FieldCredibleSetLocusElementLogBf,
            FieldCredibleSetLocusElementBeta,
            FieldCredibleSetLocusElementStandardError,
            FieldCredibleSetLocusElementPValueMantissa,
            FieldCredibleSetLocusElementPValueExponent,
        ],
    )
)
