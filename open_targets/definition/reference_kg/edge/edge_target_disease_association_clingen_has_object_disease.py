"""Summary: TARGET_DISEASE_ASSOCIATION_CLINGEN -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_clingen -> disease):
links each TARGET_DISEASE_ASSOCIATION_CLINGEN node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceClingen,
    FieldEvidenceClingenDiseaseId,
    FieldEvidenceClingenId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_clingen_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceClingen),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceClingenId,
        target=FieldEvidenceClingenDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
