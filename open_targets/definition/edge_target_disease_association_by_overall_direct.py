"""Acquisition definition that acquires direct associations between targets and diseases overall."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByOverallDirect,
    FieldAssociationByOverallDirectDiseaseId,
    FieldAssociationByOverallDirectEvidenceCount,
    FieldAssociationByOverallDirectScore,
    FieldAssociationByOverallDirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_overall_direct: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByOverallDirect),
    primary_id=get_arrow_expression(FieldAssociationByOverallDirectTargetId, FieldAssociationByOverallDirectDiseaseId),
    source=FieldAssociationByOverallDirectTargetId,
    target=FieldAssociationByOverallDirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_OVERALL_DIRECT",
    properties=[
        FieldAssociationByOverallDirectEvidenceCount,
        FieldAssociationByOverallDirectScore,
    ],
)
