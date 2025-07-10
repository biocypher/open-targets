"""Acquisition definition that acquires nodes of data sources."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatasourceDirect,
    FieldAssociationByDatasourceDirectDatasourceId,
)

node_datasource: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatasourceDirect),
    primary_id=FieldAssociationByDatasourceDirectDatasourceId,
    label="DATASOURCE",
    properties=[],
)
