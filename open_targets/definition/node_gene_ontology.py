"""Acquisition definition that acquires nodes of GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetGo,
    FieldGoId,
    FieldGoName,
)

node_gene_ontology: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetGo),
    primary_id=FieldGoId,
    label="GO_TERM",
    properties=[
        FieldGoName,
    ],
)
