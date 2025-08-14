"""Acquisition definition that acquires nodes of IMPC evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.adapter.scan_operation_predicate import PushdownEqualityPredicate
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiologicalModelAllelicComposition,
    FieldEvidenceBiologicalModelGeneticBackground,
    FieldEvidenceBiologicalModelId,
    FieldEvidenceDatasourceId,
    FieldEvidenceDirectionOnTrait,
    FieldEvidenceDiseaseFromSource,
    FieldEvidenceDiseaseFromSourceId,
    FieldEvidenceDiseaseModelAssociatedHumanPhenotypes,
    FieldEvidenceDiseaseModelAssociatedModelPhenotypes,
    FieldEvidenceId,
    FieldEvidenceLiterature,
    FieldEvidenceResourceScore,
    FieldEvidenceScore,
    FieldEvidenceTargetInModel,
    FieldEvidenceTargetInModelEnsemblId,
    FieldEvidenceTargetInModelMgiId,
    FieldEvidenceVariantEffect,
)

node_evidence_impc: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(
        dataset=DatasetEvidence,
        predicate=PushdownEqualityPredicate(FieldEvidenceDatasourceId, "impc"),
    ),
    primary_id=FieldEvidenceId,
    label="IMPC_EVIDENCE",
    properties=[
        FieldEvidenceBiologicalModelAllelicComposition,
        FieldEvidenceBiologicalModelGeneticBackground,
        FieldEvidenceBiologicalModelId,
        FieldEvidenceDirectionOnTrait,
        FieldEvidenceDiseaseFromSource,
        FieldEvidenceDiseaseFromSourceId,
        FieldEvidenceDiseaseModelAssociatedHumanPhenotypes,
        FieldEvidenceDiseaseModelAssociatedModelPhenotypes,
        FieldEvidenceLiterature,
        FieldEvidenceResourceScore,
        FieldEvidenceScore,
        FieldEvidenceTargetInModel,
        FieldEvidenceTargetInModelEnsemblId,
        FieldEvidenceTargetInModelMgiId,
        FieldEvidenceVariantEffect,
    ],
)
