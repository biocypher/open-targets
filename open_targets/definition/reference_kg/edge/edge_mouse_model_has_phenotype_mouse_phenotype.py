"""Summary: MOUSE_MODEL -> MOUSE_PHENOTYPE edges (observed phenotypes).

Definition for HAS_PHENOTYPE edges (mouse model -> mouse phenotype): explodes
biologicalModels in the Mouse Phenotypes parquet to connect each MOUSE_MODEL to
its observed MOUSE_PHENOTYPE term, capturing in vivo phenotype outcomes in the
KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotype,
    FieldMousePhenotypeBiologicalModels,
    FieldMousePhenotypeBiologicalModelsElementId,
    FieldMousePhenotypeModelPhenotypeId,
)
from open_targets.definition.helper import get_null_to_dummy_string_expression
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_mouse_model_has_phenotype_mouse_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetMousePhenotype,
            exploded_field=FieldMousePhenotypeBiologicalModels,
        ),
        primary_id=NewUuidExpression(),
        source=get_null_to_dummy_string_expression(FieldMousePhenotypeBiologicalModelsElementId),
        target=get_null_to_dummy_string_expression(FieldMousePhenotypeModelPhenotypeId),
        label=EdgeLabel.HAS_PHENOTYPE,
        properties=[],
    )
)
