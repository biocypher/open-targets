"""Acquisition definition that acquires nodes of publications."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesId,
    FieldEpmcCooccurrencesProvider,
    FieldEpmcCooccurrencesSrc,
)

node_publication: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEpmcCooccurrences),
    primary_id=FieldEpmcCooccurrencesId,
    label="PUBLICATION",
    properties=[
        FieldEpmcCooccurrencesProvider,
        FieldEpmcCooccurrencesSrc,
    ],
)
