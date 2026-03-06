"""Summary: TARGET -> TARGET_PRIORITISATION edges.

Definition for HAS_PRIORITISATION edges
(target -> target_prioritisation): links each
TARGET to its TARGET_PRIORITISATION record from
the Target Engine project.
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
    DatasetTargetPrioritisation,
    FieldTargetPrioritisationTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    target_prioritisation_primary_id_expression,
)

edge_target_has_prioritisation: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargetPrioritisation),
    primary_id=NewUuidExpression(),
    source=FieldTargetPrioritisationTargetId,
    target=target_prioritisation_primary_id_expression,
    label=EdgeLabel.HAS_PRIORITISATION,
    properties=[],
)
