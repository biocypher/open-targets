"""Summary: cancer_biomarkers association -> drug response edges.

Definition for HAS_DRUG_RESPONSE edges: links cancer_biomarkers
TARGET_DISEASE_ASSOCIATION nodes (evidence id) to drug response entities from
the Evidence parquet, capturing reported drug responses tied to the biomarker
association in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import FieldExpression, NewUuidExpression, TransformExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCancerBiomarkers,
    FieldEvidenceCancerBiomarkersDrugResponse,
    FieldEvidenceCancerBiomarkersId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_cancer_biomarkers_has_drug_response_entity: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceCancerBiomarkers),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCancerBiomarkersId,
        target=TransformExpression(
            FieldExpression(FieldEvidenceCancerBiomarkersDrugResponse),
            lambda value: value.replace("_", ":", 1),
        ),
        label=EdgeLabel.HAS_DRUG_RESPONSE,
        properties=[],
    )
)
