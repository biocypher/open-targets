"""Summary: PHARMACOGENOMICS_ANNOTATION -> VARIANT edges.

Definition for HAS_VARIANT edges
(pharmacogenomics_annotation -> variant): links each
PHARMACOGENOMICS_ANNOTATION to the VARIANT
documenting its effect on drug response.
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
    DatasetPharmacogenomics,
    FieldPharmacogenomicsVariantId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

edge_pharmacogenomics_annotation_has_variant: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(
            dataset=DatasetPharmacogenomics,
            predicate=NotExpression(EqualityExpression(FieldPharmacogenomicsVariantId, None)),
        ),
        primary_id=NewUuidExpression(),
        source=pharmacogenomics_annotation_primary_id_expression,
        target=FieldPharmacogenomicsVariantId,
        label=EdgeLabel.HAS_VARIANT,
        properties=[],
    )
)
