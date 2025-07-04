"""Acquisition definition that acquires nodes of target cross-references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsDbXrefs,
    FieldTargetsDbXrefsElementId,
    FieldTargetsDbXrefsElementSource,
)

node_target_xref: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsDbXrefs,
    ),
    primary_id=FieldTargetsDbXrefsElementId,
    label="TARGET_XREF",
    properties=[
        FieldTargetsDbXrefsElementSource,
    ],
)
