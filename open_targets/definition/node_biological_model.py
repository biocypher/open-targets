"""Acquisition definition that acquires nodes of biological models."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiologicalModelId,
    FieldEvidenceBiologicalModelAllelicComposition,
    FieldEvidenceBiologicalModelGeneticBackground,
)

node_biological_model: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=FieldEvidenceBiologicalModelId,
    label="BIOLOGICAL_MODEL",
    properties=[
        FieldEvidenceBiologicalModelAllelicComposition,
        FieldEvidenceBiologicalModelGeneticBackground,
    ],
)
