"""Acquisition definition that acquires nodes of Europe PMC evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceId,
    FieldEvidencePublicationYear,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
)

node_evidence_europepmc: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "europepmc"),
    ),
    primary_id=FieldEvidenceId,
    label="EUROPEPMC_EVIDENCE",
    properties=[
        FieldEvidencePublicationYear,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
    ],
)
