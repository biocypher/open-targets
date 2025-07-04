"""Acquisition definition that acquires nodes of adverse reactions."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAdverseDrugReactions,
    FieldAdverseDrugReactionsMeddraCode,
    FieldAdverseDrugReactionsReactionReactionmeddrapt,
)

node_adverse_reaction: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAdverseDrugReactions),
    primary_id=FieldAdverseDrugReactionsMeddraCode,
    label="ADVERSE_REACTION",
    properties=[
        FieldAdverseDrugReactionsReactionReactionmeddrapt,
    ],
)
