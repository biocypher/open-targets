"""Summary: TARGET_DISEASE_ASSOCIATION_CANCER_BIOMARKERS -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_cancer_biomarkers -> disease):
links each TARGET_DISEASE_ASSOCIATION_CANCER_BIOMARKERS node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCancerBiomarkers,
    FieldEvidenceCancerBiomarkersDiseaseId,
    FieldEvidenceCancerBiomarkersId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_cancer_biomarkers_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceCancerBiomarkers),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCancerBiomarkersId,
        target=FieldEvidenceCancerBiomarkersDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
