"""Acquisition definition that acquires nodes of mouse targets."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesTargetFromSourceId,
    FieldMousePhenotypesTargetInModel,
    FieldMousePhenotypesTargetInModelEnsemblId,
    FieldMousePhenotypesTargetInModelMgiId,
)

node_mouse_target: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=FieldMousePhenotypesTargetInModelEnsemblId,
    label="MOUSE_TARGET",
    properties=[
        FieldMousePhenotypesTargetInModel,
        FieldMousePhenotypesTargetInModelMgiId,
        FieldMousePhenotypesTargetFromSourceId,
    ],
)
