"""Summary: PHARMACOGENOMICS_ANNOTATION -> TARGET edges.

Definition for HAS_TARGET edges
(pharmacogenomics_annotation -> target): links each
PHARMACOGENOMICS_ANNOTATION to the TARGET it
concerns.
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
    FieldPharmacogenomicsTargetFromSourceId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

edge_pharmacogenomics_annotation_has_target: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(
            dataset=DatasetPharmacogenomics,
            predicate=NotExpression(EqualityExpression(FieldPharmacogenomicsTargetFromSourceId, None)),
        ),
        primary_id=NewUuidExpression(),
        source=pharmacogenomics_annotation_primary_id_expression,
        target=FieldPharmacogenomicsTargetFromSourceId,
        label=EdgeLabel.HAS_TARGET,
        properties=[],
    )
)
