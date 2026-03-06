"""Summary: TARGET_DISEASE_ASSOCIATION_CRISPR -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_crispr -> disease):
links each TARGET_DISEASE_ASSOCIATION_CRISPR node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCrispr,
    FieldEvidenceCrisprDiseaseId,
    FieldEvidenceCrisprId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_crispr_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceCrispr),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCrisprId,
        target=FieldEvidenceCrisprDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
