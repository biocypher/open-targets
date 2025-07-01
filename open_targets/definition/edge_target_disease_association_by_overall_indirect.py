"""Acquisition definition that acquires indirect associations between targets and diseases overall."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByOverallIndirect,
    FieldAssociationByOverallIndirectDiseaseId,
    FieldAssociationByOverallIndirectEvidenceCount,
    FieldAssociationByOverallIndirectScore,
    FieldAssociationByOverallIndirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_overall_indirect: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByOverallIndirect),
    primary_id=get_arrow_expression(FieldAssociationByOverallIndirectTargetId, FieldAssociationByOverallIndirectDiseaseId),
    source=FieldAssociationByOverallIndirectTargetId,
    target=FieldAssociationByOverallIndirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_OVERALL_INDIRECT",
    properties=[
        FieldAssociationByOverallIndirectEvidenceCount,
        FieldAssociationByOverallIndirectScore,
    ],
)
