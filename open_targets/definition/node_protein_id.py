"""Acquisition definition that acquires nodes of protein identifiers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsProteinIds,
    FieldTargetsProteinIdsElementId,
    FieldTargetsProteinIdsElementSource,
)

node_protein_id: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsProteinIds,
    ),
    primary_id=FieldTargetsProteinIdsElementId,
    label="PROTEIN_ID",
    properties=[
        FieldTargetsProteinIdsElementSource,
    ],
)
