"""Summary: MOUSE_PHENOTYPE -> MOUSE_PHENOTYPE classification edges.

Definition for CLASSIFIED_AS edges: explodes phenotype class annotations in
Mouse Phenotypes parquet to link each observed MOUSE_PHENOTYPE to its broader MP
class term, both represented under the canonical MOUSE_PHENOTYPE node label.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotype,
    FieldMousePhenotypeModelPhenotypeClasses,
    FieldMousePhenotypeModelPhenotypeClassesElementId,
    FieldMousePhenotypeModelPhenotypeId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_mouse_phenotype_classified_as_mouse_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetMousePhenotype,
            exploded_field=FieldMousePhenotypeModelPhenotypeClasses,
        ),
        primary_id=NewUuidExpression(),
        source=FieldMousePhenotypeModelPhenotypeId,
        target=FieldMousePhenotypeModelPhenotypeClassesElementId,
        label=EdgeLabel.CLASSIFIED_AS,
        properties=[],
    )
)
