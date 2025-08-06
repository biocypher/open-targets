"""Acquisition definition that acquires nodes of HPO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetHpo,
    FieldHpoDbXRefs,
    FieldHpoDescription,
    FieldHpoId,
    FieldHpoName,
    FieldHpoNamespace,
    FieldHpoObsoleteTerms,
)

node_hpo_term: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetHpo),
    primary_id=FieldHpoId,
    label="HPO_TERM",
    properties=[
        FieldHpoName,
        FieldHpoDescription,
        FieldHpoDbXRefs,
        FieldHpoNamespace,
        FieldHpoObsoleteTerms,
    ],
)
