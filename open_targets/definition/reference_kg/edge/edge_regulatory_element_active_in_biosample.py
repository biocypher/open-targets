"""Summary: REGULATORY_ELEMENT -> BIOSAMPLE edges.

Definition for ACTIVE_IN edges
(regulatory_element -> biosample): links each
REGULATORY_ELEMENT to the BIOSAMPLE (tissue)
in which it is active.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEnhancerToGene,
    FieldEnhancerToGeneBiosampleId,
    FieldEnhancerToGeneIntervalId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_regulatory_element_active_in_biosample: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEnhancerToGene),
        primary_id=NewUuidExpression(),
        source=FieldEnhancerToGeneIntervalId,
        target=FieldEnhancerToGeneBiosampleId,
        label=EdgeLabel.ACTIVE_IN,
        properties=[],
    )
)
