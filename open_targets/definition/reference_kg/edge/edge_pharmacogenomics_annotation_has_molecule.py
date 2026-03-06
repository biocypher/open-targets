"""Summary: PHARMACOGENOMICS_ANNOTATION -> MOLECULE edges.

Definition for HAS_MOLECULE edges
(pharmacogenomics_annotation -> molecule): explodes
the drugs array to link each
PHARMACOGENOMICS_ANNOTATION to its referenced
MOLECULE (drug).
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
    DatasetPharmacogenomics,
    FieldPharmacogenomicsDrugs,
    FieldPharmacogenomicsDrugsElementDrugId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

edge_pharmacogenomics_annotation_has_molecule: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetPharmacogenomics,
            exploded_field=FieldPharmacogenomicsDrugs,
        ),
        primary_id=NewUuidExpression(),
        source=pharmacogenomics_annotation_primary_id_expression,
        target=FieldPharmacogenomicsDrugsElementDrugId,
        label=EdgeLabel.HAS_MOLECULE,
        properties=[],
    )
)
