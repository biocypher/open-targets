"""Summary: TARGET -> TARGET_DISEASE_ASSOCIATION_CHEMBL edges.

Definition for SUBJECT_OF edges (target -> target_disease_association_chembl):
links each TARGET to the TARGET_DISEASE_ASSOCIATION_CHEMBL nodes it is the subject of.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceChembl,
    FieldEvidenceChemblId,
    FieldEvidenceChemblTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_subject_of_target_disease_association_chembl: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceChembl),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceChemblTargetId,
        target=FieldEvidenceChemblId,
        label=EdgeLabel.SUBJECT_OF,
        properties=[],
    )
)
