"""Acquisition definition that acquires nodes of UniProt literature evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceConfidence,
    FieldEvidenceDatasourceId,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceScore,
    FieldEvidenceTargetModulation,
)

node_evidence_uniprot_literature: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "uniprot_literature"),
    ),
    primary_id=FieldEvidenceId,
    label="UNIPROT_LITERATURE_EVIDENCE",
    properties=[
        FieldEvidenceConfidence,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceLiterature,
        FieldEvidenceScore,
        FieldEvidenceTargetModulation,
    ],
)
