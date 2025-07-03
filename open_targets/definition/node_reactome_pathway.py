"""Acquisition definition that acquires nodes of Reactome pathways."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetReactome,
    FieldReactomeId,
    FieldReactomeLabel,
)

node_reactome_pathway: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetReactome),
    primary_id=FieldReactomeId,
    label="REACTOME_PATHWAY",
    properties=[
        FieldReactomeLabel,
    ],
)
