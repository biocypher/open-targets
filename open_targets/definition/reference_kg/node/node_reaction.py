"""Summary: Reactome reaction nodes (id/name) for pathway inference.

Definition for REACTION nodes: extracts reaction IDs and names from Reactome
evidence records, providing the reaction entities referenced by pathway
annotations in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceReactome,
    FieldEvidenceReactomeReactionId,
    FieldEvidenceReactomeReactionName,
)

node_reaction: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidenceReactome),
    primary_id=FieldEvidenceReactomeReactionId,
    label="REACTION",
    properties=[
        FieldEvidenceReactomeReactionName,
    ],
)
