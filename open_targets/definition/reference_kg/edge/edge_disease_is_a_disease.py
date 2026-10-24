"""Summary: DISEASE hierarchy IS_A edges (child -> parent).

Definition for IS_A edges (disease hierarchy): explodes parent relationships in
the diseases parquet to link each DISEASE node to its parent DISEASE, forming
the ontology hierarchy in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDisease,
    FieldDiseaseId,
    FieldDiseaseParents,
    FieldDiseaseParentsElement,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_disease_is_a_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDisease,
        exploded_field=FieldDiseaseParents,
    ),
    primary_id=NewUuidExpression(),
    source=FieldDiseaseId,
    target=FieldDiseaseParentsElement,
    label=EdgeLabel.IS_A,
    properties=[],
)
