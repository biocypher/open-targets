"""Summary: TARGET_DISEASE_ASSOCIATION_GENE_BURDEN -> DISEASE edges.

Definition for HAS_OBJECT edges (target_disease_association_gene_burden -> disease):
links each TARGET_DISEASE_ASSOCIATION_GENE_BURDEN node to the DISEASE it references.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceGeneBurden,
    FieldEvidenceGeneBurdenDiseaseId,
    FieldEvidenceGeneBurdenId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_gene_burden_has_object_disease: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceGeneBurden),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceGeneBurdenId,
        target=FieldEvidenceGeneBurdenDiseaseId,
        label=EdgeLabel.HAS_OBJECT,
        properties=[],
    )
)
