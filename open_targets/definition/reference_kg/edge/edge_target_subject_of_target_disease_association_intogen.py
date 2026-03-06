"""Summary: TARGET -> TARGET_DISEASE_ASSOCIATION_INTOGEN edges.

Definition for SUBJECT_OF edges (target -> target_disease_association_intogen):
links each TARGET to the TARGET_DISEASE_ASSOCIATION_INTOGEN nodes it is the subject of.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceIntogen,
    FieldEvidenceIntogenId,
    FieldEvidenceIntogenTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_subject_of_target_disease_association_intogen: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceIntogen),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceIntogenTargetId,
        target=FieldEvidenceIntogenId,
        label=EdgeLabel.SUBJECT_OF,
        properties=[],
    )
)
