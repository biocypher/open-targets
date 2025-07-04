"""Acquisition definition that acquires nodes of HPO phenotypes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetHpo,
    FieldHpoId,
    FieldHpoName,
    FieldHpoDescription,
)

node_hpo_phenotype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetHpo),
    primary_id=FieldHpoId,
    label="HPO_PHENOTYPE",
    properties=[
        FieldHpoName,
        FieldHpoDescription,
    ],
)
