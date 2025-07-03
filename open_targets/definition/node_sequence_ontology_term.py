"""Acquisition definition that acquires nodes of Sequence Ontology terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetSo,
    FieldSoId,
    FieldSoLabel,
)

node_sequence_ontology_term: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetSo),
    primary_id=FieldSoId,
    label="SEQUENCE_ONTOLOGY_TERM",
    properties=[
        FieldSoLabel,
    ],
)
