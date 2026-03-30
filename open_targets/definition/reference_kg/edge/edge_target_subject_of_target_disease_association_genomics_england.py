"""Summary: TARGET -> TARGET_DISEASE_ASSOCIATION_GENOMICS_ENGLAND edges.

Definition for SUBJECT_OF edges (target -> target_disease_association_genomics_england):
links each TARGET to the TARGET_DISEASE_ASSOCIATION_GENOMICS_ENGLAND nodes it is the subject of.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceGenomicsEngland,
    FieldEvidenceGenomicsEnglandId,
    FieldEvidenceGenomicsEnglandTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_subject_of_target_disease_association_genomics_england: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceGenomicsEngland),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceGenomicsEnglandTargetId,
        target=FieldEvidenceGenomicsEnglandId,
        label=EdgeLabel.SUBJECT_OF,
        properties=[],
    )
)
