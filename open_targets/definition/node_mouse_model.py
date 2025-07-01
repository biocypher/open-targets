"""Acquisition definition that acquires nodes of mouse models."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesBiologicalModels,
    FieldMousePhenotypesModelPhenotypeClasses,
)

node_mouse_model: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=FieldMousePhenotypesBiologicalModels,
    label="MOUSE_MODEL",
    properties=[
        FieldMousePhenotypesModelPhenotypeClasses,
    ],
)
