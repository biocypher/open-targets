"""Acquisition definition that acquires indirect associations between targets and diseases by datatype."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatatypeIndirect,
    FieldAssociationByDatatypeIndirectDatatypeId,
    FieldAssociationByDatatypeIndirectDiseaseId,
    FieldAssociationByDatatypeIndirectEvidenceCount,
    FieldAssociationByDatatypeIndirectScore,
    FieldAssociationByDatatypeIndirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_datatype_indirect: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatatypeIndirect),
    primary_id=get_arrow_expression(FieldAssociationByDatatypeIndirectTargetId, FieldAssociationByDatatypeIndirectDiseaseId),
    source=FieldAssociationByDatatypeIndirectTargetId,
    target=FieldAssociationByDatatypeIndirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_DATATYPE_INDIRECT",
    properties=[
        FieldAssociationByDatatypeIndirectDatatypeId,
        FieldAssociationByDatatypeIndirectEvidenceCount,
        FieldAssociationByDatatypeIndirectScore,
    ],
)
