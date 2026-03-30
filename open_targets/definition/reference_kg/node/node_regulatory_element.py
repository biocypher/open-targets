"""Summary: regulatory element nodes from enhancer data.

Definition for REGULATORY_ELEMENT nodes: scans the
enhancer_to_gene parquet to emit genomic regulatory
regions (enhancers, promoters) with their genomic
coordinates, type, score, and associated metadata.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEnhancerToGene,
    FieldEnhancerToGeneChromosome,
    FieldEnhancerToGeneDatasourceId,
    FieldEnhancerToGeneDistanceToTss,
    FieldEnhancerToGeneEnd,
    FieldEnhancerToGeneIntervalId,
    FieldEnhancerToGeneIntervalType,
    FieldEnhancerToGeneScore,
    FieldEnhancerToGeneStart,
    FieldEnhancerToGeneStudyId,
)

node_regulatory_element: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEnhancerToGene),
    primary_id=FieldEnhancerToGeneIntervalId,
    label="REGULATORY_ELEMENT",
    properties=[
        FieldEnhancerToGeneChromosome,
        FieldEnhancerToGeneStart,
        FieldEnhancerToGeneEnd,
        FieldEnhancerToGeneIntervalType,
        FieldEnhancerToGeneDistanceToTss,
        FieldEnhancerToGeneScore,
        FieldEnhancerToGeneDatasourceId,
        FieldEnhancerToGeneStudyId,
    ],
)
