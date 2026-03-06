"""Summary: GENETIC_ASSOCIATION_STUDY REPORTS_TRAIT DISEASE edge.

Definition for REPORTS_TRAIT edge: Connects a GENETIC_ASSOCIATION_STUDY
to a DISEASE representing the mapped trait evaluated in the study.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetStudy,
    FieldStudyDiseaseIds,
    FieldStudyDiseaseIdsElement,
    FieldStudyStudyId,
)
from open_targets.definition.helper import get_null_to_dummy_string_expression
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_genetic_association_study_reports_trait_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetStudy,
            exploded_field=FieldStudyDiseaseIds,
        ),
        primary_id=NewUuidExpression(),
        source=FieldStudyStudyId,
        target=get_null_to_dummy_string_expression(FieldStudyDiseaseIdsElement),
        label=EdgeLabel.REPORTS_TRAIT,
        properties=[],
    )
)
