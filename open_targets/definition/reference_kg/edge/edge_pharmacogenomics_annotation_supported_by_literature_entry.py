"""Summary: PHARMACOGENOMICS_ANNOTATION -> LITERATURE edges.

Definition for SUPPORTED_BY edges
(pharmacogenomics_annotation -> literature_entry):
explodes the literature array to link each
PHARMACOGENOMICS_ANNOTATION record to its supporting
PubMed references.
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
    FieldPharmacogenomicsLiterature,
    FieldPharmacogenomicsLiteratureElement,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

edge_pharmacogenomics_annotation_supported_by_literature_entry: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetPharmacogenomics,
            exploded_field=FieldPharmacogenomicsLiterature,
        ),
        primary_id=NewUuidExpression(),
        source=pharmacogenomics_annotation_primary_id_expression,
        target=FieldPharmacogenomicsLiteratureElement,
        label=EdgeLabel.SUPPORTED_BY,
        properties=[],
    )
)
