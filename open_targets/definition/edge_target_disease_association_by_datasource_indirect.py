"""Acquisition definition that acquires indirect associations between targets and diseases by datasource."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatasourceIndirect,
    FieldAssociationByDatasourceIndirectDatasourceId,
    FieldAssociationByDatasourceIndirectDatatypeId,
    FieldAssociationByDatasourceIndirectDiseaseId,
    FieldAssociationByDatasourceIndirectEvidenceCount,
    FieldAssociationByDatasourceIndirectScore,
    FieldAssociationByDatasourceIndirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_datasource_indirect: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatasourceIndirect),
    primary_id=get_arrow_expression(FieldAssociationByDatasourceIndirectTargetId, FieldAssociationByDatasourceIndirectDiseaseId),
    source=FieldAssociationByDatasourceIndirectTargetId,
    target=FieldAssociationByDatasourceIndirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_DATASOURCE_INDIRECT",
    properties=[
        FieldAssociationByDatasourceIndirectDatasourceId,
        FieldAssociationByDatasourceIndirectDatatypeId,
        FieldAssociationByDatasourceIndirectEvidenceCount,
        FieldAssociationByDatasourceIndirectScore,
    ],
)
