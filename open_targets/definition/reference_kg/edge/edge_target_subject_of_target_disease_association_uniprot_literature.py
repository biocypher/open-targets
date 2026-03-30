"""Summary: TARGET -> TARGET_DISEASE_ASSOCIATION_UNIPROT_LITERATURE edges.

Definition for SUBJECT_OF edges (target -> target_disease_association_uniprot_literature):
links each TARGET to the TARGET_DISEASE_ASSOCIATION_UNIPROT_LITERATURE nodes it is the subject of.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceUniprotLiterature,
    FieldEvidenceUniprotLiteratureId,
    FieldEvidenceUniprotLiteratureTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_subject_of_target_disease_association_uniprot_literature: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceUniprotLiterature),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceUniprotLiteratureTargetId,
        target=FieldEvidenceUniprotLiteratureId,
        label=EdgeLabel.SUBJECT_OF,
        properties=[],
    )
)
