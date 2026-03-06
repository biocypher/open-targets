"""Summary: TARGET_DISEASE_ASSOCIATION_ORPHANET -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_orphanet -> disease):
links each TARGET_DISEASE_ASSOCIATION_ORPHANET node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceOrphanet,
    FieldEvidenceOrphanetDiseaseId,
    FieldEvidenceOrphanetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_orphanet_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceOrphanet),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceOrphanetId,
        target=FieldEvidenceOrphanetDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
