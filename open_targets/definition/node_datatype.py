"""Acquisition definition that acquires nodes of data types."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAssociationByDatatypeDirect,
    FieldAssociationByDatatypeDirectDatatypeId,
)

node_datatype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAssociationByDatatypeDirect),
    primary_id=FieldAssociationByDatatypeDirectDatatypeId,
    label="DATATYPE",
    properties=[],
)
