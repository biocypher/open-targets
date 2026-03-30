"""Summary: TARGET_DISEASE_ASSOCIATION_EXPRESSION_ATLAS -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_expression_atlas -> disease):
links each TARGET_DISEASE_ASSOCIATION_EXPRESSION_ATLAS node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceExpressionAtlas,
    FieldEvidenceExpressionAtlasDiseaseId,
    FieldEvidenceExpressionAtlasId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_expression_atlas_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceExpressionAtlas),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceExpressionAtlasId,
        target=FieldEvidenceExpressionAtlasDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
