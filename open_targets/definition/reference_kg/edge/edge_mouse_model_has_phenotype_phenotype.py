"""Summary: MOUSE_MODEL -> PHENOTYPE (HPO) edges (cross-species phenotypes).

Definition for HAS_PHENOTYPE edges (mouse model -> human phenotype): explodes
IMPC evidence human phenotype annotations to link each MOUSE_MODEL to HPO
PHENOTYPE terms, capturing cross-species phenotype observations in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import FieldExpression, NewUuidExpression, TransformExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.scan_operation_predicate import EqualityExpression, NotExpression
from open_targets.data.schema import (
    DatasetEvidenceImpc,
    FieldEvidenceImpcBiologicalModelId,
    FieldEvidenceImpcDiseaseModelAssociatedHumanPhenotypes,
    FieldEvidenceImpcDiseaseModelAssociatedHumanPhenotypesElementId,
)
from open_targets.definition.helper import get_namespaced_expression
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_mouse_model_has_phenotype_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidenceImpc,
        exploded_field=FieldEvidenceImpcDiseaseModelAssociatedHumanPhenotypes,
        predicate=NotExpression(EqualityExpression(FieldEvidenceImpcBiologicalModelId, None)),
    ),
    primary_id=NewUuidExpression(),
    source=FieldEvidenceImpcBiologicalModelId,
    target=get_namespaced_expression(
        "phenotype",
        TransformExpression(
            FieldExpression(FieldEvidenceImpcDiseaseModelAssociatedHumanPhenotypesElementId),
            lambda value: value.replace(":", "_", 1),
        ),
    ),
    label=EdgeLabel.HAS_PHENOTYPE,
    properties=[],
)
