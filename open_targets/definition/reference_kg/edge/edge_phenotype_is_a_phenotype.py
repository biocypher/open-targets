"""Summary: PHENOTYPE hierarchy IS_A edges (child -> parent).

Definition for IS_A edges (phenotype hierarchy): explodes HPO parents to link
each PHENOTYPE node to its parent PHENOTYPE, forming the HPO ontology in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseaseHpo,
    FieldDiseaseHpoId,
    FieldDiseaseHpoParents,
    FieldDiseaseHpoParentsElement,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_phenotype_is_a_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseaseHpo,
        exploded_field=FieldDiseaseHpoParents,
    ),
    primary_id=NewUuidExpression(),
    source=FieldDiseaseHpoId,
    target=FieldDiseaseHpoParentsElement,
    label=EdgeLabel.IS_A,
    properties=[],
)
