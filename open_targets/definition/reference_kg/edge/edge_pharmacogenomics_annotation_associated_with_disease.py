"""Summary: PHARMACOGENOMICS_ANNOTATION -> DISEASE edges.

Definition for ASSOCIATED_WITH edges
(pharmacogenomics_annotation -> disease): links each
PHARMACOGENOMICS_ANNOTATION to the DISEASE
(phenotype) it describes.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetPharmacogenomics,
    FieldPharmacogenomicsPhenotypeFromSourceId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

edge_pharmacogenomics_annotation_associated_with_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetPharmacogenomics),
        primary_id=NewUuidExpression(),
        source=pharmacogenomics_annotation_primary_id_expression,
        target=FieldPharmacogenomicsPhenotypeFromSourceId,
        label=EdgeLabel.ASSOCIATED_WITH,
        properties=[],
    )
)
