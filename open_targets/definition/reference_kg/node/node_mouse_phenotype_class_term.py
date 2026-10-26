"""Summary: MP phenotype class terms emitted as canonical phenotype nodes.

Definition for MOUSE_PHENOTYPE nodes from class annotations: explodes phenotype
class entries from the Mouse Phenotypes parquet and emits each MP class term
under the canonical MOUSE_PHENOTYPE label. Class relationships are represented
by CLASSIFIED_AS edges.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotype,
    FieldMousePhenotypeModelPhenotypeClasses,
    FieldMousePhenotypeModelPhenotypeClassesElementId,
    FieldMousePhenotypeModelPhenotypeClassesElementLabel,
)

node_mouse_phenotype_class_term: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMousePhenotype,
        exploded_field=FieldMousePhenotypeModelPhenotypeClasses,
    ),
    primary_id=FieldMousePhenotypeModelPhenotypeClassesElementId,
    label="MOUSE_PHENOTYPE",
    properties=[
        FieldMousePhenotypeModelPhenotypeClassesElementLabel,
    ],
)
