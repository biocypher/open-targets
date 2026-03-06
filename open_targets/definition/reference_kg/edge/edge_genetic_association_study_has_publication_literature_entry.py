"""Summary: GENETIC_ASSOCIATION_STUDY HAS LiteratureEntry edge.

Definition for HAS_PUBLICATION edge: Connects a GENETIC_ASSOCIATION_STUDY
to its LiteratureEntry via pubmedId.
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
from open_targets.definition.reference_kg.expression import study_literature_expression

edge_genetic_association_study_has_publication_literature_entry: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetStudy),
        primary_id=NewUuidExpression(),
        source=FieldStudyStudyId,
        target=study_literature_expression,
        label=EdgeLabel.HAS_PUBLICATION,
        properties=[],
    )
)
