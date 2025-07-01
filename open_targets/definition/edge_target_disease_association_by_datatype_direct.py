"""Acquisition definition that acquires direct associations between targets and diseases by datatype."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatatypeDirect,
    FieldAssociationByDatatypeDirectDatatypeId,
    FieldAssociationByDatatypeDirectDiseaseId,
    FieldAssociationByDatatypeDirectEvidenceCount,
    FieldAssociationByDatatypeDirectScore,
    FieldAssociationByDatatypeDirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_datatype_direct: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatatypeDirect),
    primary_id=get_arrow_expression(FieldAssociationByDatatypeDirectTargetId, FieldAssociationByDatatypeDirectDiseaseId),
    source=FieldAssociationByDatatypeDirectTargetId,
    target=FieldAssociationByDatatypeDirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_DATATYPE_DIRECT",
    properties=[
        FieldAssociationByDatatypeDirectDatatypeId,
        FieldAssociationByDatatypeDirectEvidenceCount,
        FieldAssociationByDatatypeDirectScore,
    ],
)
