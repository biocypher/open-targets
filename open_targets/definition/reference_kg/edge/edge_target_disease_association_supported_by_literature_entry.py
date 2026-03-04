"""Summary: TARGET_DISEASE_ASSOCIATION -> LITERATURE_ENTRY support edges (cancer_biomarkers).

Definition for SUPPORTED_BY edges: for cancer_biomarkers evidence, explodes gene
expression biomarker literature references to link each TARGET_DISEASE_ASSOCIATION
node (evidence id) to a supporting LITERATURE_ENTRY (hashed id), capturing
literature provenance for the association in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCancerBiomarkers,
    FieldEvidenceCancerBiomarkersBiomarkersGeneExpression,
    FieldEvidenceCancerBiomarkersId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import target_disease_association_literature_entry_expression

edge_target_disease_association_supported_by_literature_entry: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetEvidenceCancerBiomarkers,
            exploded_field=FieldEvidenceCancerBiomarkersBiomarkersGeneExpression,
        ),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCancerBiomarkersId,
        target=target_disease_association_literature_entry_expression,
        label=EdgeLabel.SUPPORTED_BY,
        properties=[],
    )
)
