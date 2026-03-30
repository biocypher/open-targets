"""Summary: TARGET_DISEASE_ASSOCIATION -> MOUSE_MODEL inference edges (IMPC).

Definition for INFERRED_FROM edges (association -> mouse model): filters IMPC
evidence to link each TARGET_DISEASE_ASSOCIATION node (evidence id) to the
MOUSE_MODEL it was inferred from, capturing the in vivo inference source in the
KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import EqualityExpression, NotExpression
from open_targets.data.schema import (
    DatasetEvidenceImpc,
    FieldEvidenceImpcBiologicalModelId,
    FieldEvidenceImpcId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_inferred_from_mouse_model: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(
            dataset=DatasetEvidenceImpc,
            predicate=NotExpression(EqualityExpression(FieldEvidenceImpcBiologicalModelId, None)),
        ),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceImpcId,
        target=FieldEvidenceImpcBiologicalModelId,
        label=EdgeLabel.INFERRED_FROM,
        properties=[],
    )
)
