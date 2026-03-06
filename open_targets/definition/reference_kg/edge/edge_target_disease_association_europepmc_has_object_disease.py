"""Summary: TARGET_DISEASE_ASSOCIATION_EUROPEPMC -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_europepmc -> disease):
links each TARGET_DISEASE_ASSOCIATION_EUROPEPMC node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceEuropepmc,
    FieldEvidenceEuropepmcDiseaseId,
    FieldEvidenceEuropepmcId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_europepmc_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceEuropepmc),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceEuropepmcId,
        target=FieldEvidenceEuropepmcDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
