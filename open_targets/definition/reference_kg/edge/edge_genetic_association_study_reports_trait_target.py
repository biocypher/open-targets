"""Summary: GENETIC_ASSOCIATION_STUDY REPORTS_TRAIT TARGET edge.

Definition for REPORTS_TRAIT edge: Connects a GENETIC_ASSOCIATION_STUDY
to a TARGET representing the gene analyzed in molecular QTL studies.
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
    DatasetStudy,
    FieldStudyGeneId,
    FieldStudyStudyId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_genetic_association_study_reports_trait_target: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetStudy),
        primary_id=NewUuidExpression(),
        source=FieldStudyStudyId,
        target=FieldStudyGeneId,
        label=EdgeLabel.REPORTS_TRAIT,
        properties=[],
    )
)
