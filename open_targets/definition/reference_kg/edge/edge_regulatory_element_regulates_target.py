"""Summary: REGULATORY_ELEMENT -> TARGET edges.

Definition for REGULATES edges
(regulatory_element -> target): links each
REGULATORY_ELEMENT to the TARGET (gene) it
regulates.
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
    FieldEnhancerToGeneGeneId,
    FieldEnhancerToGeneIntervalId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_regulatory_element_regulates_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEnhancerToGene),
    primary_id=NewUuidExpression(),
    source=FieldEnhancerToGeneIntervalId,
    target=FieldEnhancerToGeneGeneId,
    label=EdgeLabel.REGULATES,
    properties=[],
)
