"""Acquisition definition that acquires direct associations between targets and diseases by datasource."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatasourceDirect,
    FieldAssociationByDatasourceDirectDatasourceId,
    FieldAssociationByDatasourceDirectDatatypeId,
    FieldAssociationByDatasourceDirectDiseaseId,
    FieldAssociationByDatasourceDirectEvidenceCount,
    FieldAssociationByDatasourceDirectScore,
    FieldAssociationByDatasourceDirectTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_association_by_datasource_direct: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatasourceDirect),
    primary_id=get_arrow_expression(FieldAssociationByDatasourceDirectTargetId, FieldAssociationByDatasourceDirectDiseaseId),
    source=FieldAssociationByDatasourceDirectTargetId,
    target=FieldAssociationByDatasourceDirectDiseaseId,
    label="TARGET_DISEASE_ASSOCIATION_BY_DATASOURCE_DIRECT",
    properties=[
        FieldAssociationByDatasourceDirectDatasourceId,
        FieldAssociationByDatasourceDirectDatatypeId,
        FieldAssociationByDatasourceDirectEvidenceCount,
        FieldAssociationByDatasourceDirectScore,
    ],
)
