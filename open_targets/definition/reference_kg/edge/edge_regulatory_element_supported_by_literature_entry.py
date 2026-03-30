"""Summary: REGULATORY_ELEMENT -> LITERATURE edges.

Definition for SUPPORTED_BY edges
(regulatory_element -> literature_entry): links
each REGULATORY_ELEMENT to the LITERATURE_ENTRY
(PubMed reference) supporting its discovery.
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
    FieldEnhancerToGeneIntervalId,
    FieldEnhancerToGenePmid,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_regulatory_element_supported_by_literature_entry: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEnhancerToGene),
        primary_id=NewUuidExpression(),
        source=FieldEnhancerToGeneIntervalId,
        target=FieldEnhancerToGenePmid,
        label=EdgeLabel.SUPPORTED_BY,
        properties=[],
    )
)
