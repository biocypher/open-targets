"""Summary: Edge connecting GENETIC_ASSOCIATION_STUDY node to LITERATURE_ENTRY node.

Definition for edge: GENETIC_ASSOCIATION_STUDY -> LITERATURE_ENTRY
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import DatasetStudy, FieldStudyStudyId
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    genetic_association_study_literature_entry_expression,
)

edge_genetic_association_study_published_in_literature_entry: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetStudy),
        primary_id=NewUuidExpression(),
        source=FieldStudyStudyId,
        target=genetic_association_study_literature_entry_expression,
        label=EdgeLabel.PUBLISHED_IN,
        properties=[],
    )
)
