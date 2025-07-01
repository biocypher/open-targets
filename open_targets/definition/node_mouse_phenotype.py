"""Acquisition definition that acquires nodes of mouse phenotypes."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesModelPhenotypeId,
    FieldMousePhenotypesModelPhenotypeLabel,
)

node_mouse_phenotype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=FieldMousePhenotypesModelPhenotypeId,
    label="MOUSE_PHENOTYPE",
    properties=[
        FieldMousePhenotypesModelPhenotypeLabel,
    ],
)
