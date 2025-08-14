"""Acquisition definition that acquires nodes of PROGENY evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceId,
    FieldEvidencePathways,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
)

node_evidence_progeny: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "progeny"),
    ),
    primary_id=FieldEvidenceId,
    label="PROGENY_EVIDENCE",
    properties=[
        FieldEvidenceDiseaseFromSource,
        FieldEvidencePathways,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
    ],
)
