"""Summary: GENETIC_ASSOCIATION_STUDY MEASURED_IN BIOSAMPLE edge.

Definition for MEASURED_IN edge: Connects a GENETIC_ASSOCIATION_STUDY
to a BIOSAMPLE where the molecular trait was measured.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import EqualityExpression, NotExpression
from open_targets.data.schema import (
    DatasetStudy,
    FieldStudyBiosampleId,
    FieldStudyStudyId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_genetic_association_study_measured_in_biosample: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(
            dataset=DatasetStudy,
            predicate=NotExpression(EqualityExpression(FieldStudyBiosampleId, None)),
        ),
        primary_id=NewUuidExpression(),
        source=FieldStudyStudyId,
        target=FieldStudyBiosampleId,
        label=EdgeLabel.MEASURED_IN,
        properties=[],
    )
)
