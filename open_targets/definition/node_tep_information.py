"""Acquisition definition that acquires nodes of TEP information."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsTepDescription,
    FieldTargetsTepTargetFromSourceId,
    FieldTargetsTepTherapeuticArea,
    FieldTargetsTepUrl,
)

node_tep_information: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargets),
    primary_id=FieldTargetsTepTargetFromSourceId,
    label="TEP_INFORMATION",
    properties=[
        FieldTargetsTepDescription,
        FieldTargetsTepTherapeuticArea,
        FieldTargetsTepUrl,
    ],
)
