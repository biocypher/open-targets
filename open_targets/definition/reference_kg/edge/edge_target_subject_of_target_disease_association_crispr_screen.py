"""Summary: TARGET -> TARGET_DISEASE_ASSOCIATION_CRISPR_SCREEN edges.

Definition for SUBJECT_OF edges (target -> target_disease_association_crispr_screen):
links each TARGET to the TARGET_DISEASE_ASSOCIATION_CRISPR_SCREEN nodes it is the subject of.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCrisprScreen,
    FieldEvidenceCrisprScreenId,
    FieldEvidenceCrisprScreenTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_subject_of_target_disease_association_crispr_screen: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceCrisprScreen),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCrisprScreenTargetId,
        target=FieldEvidenceCrisprScreenId,
        label=EdgeLabel.SUBJECT_OF,
        properties=[],
    )
)
