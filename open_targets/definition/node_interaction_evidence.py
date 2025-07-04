"""Acquisition definition that acquires nodes of interaction evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetInteractionEvidence,
    FieldInteractionEvidenceEvidenceScore,
    FieldInteractionEvidenceExpansionMethodMiIdentifier,
    FieldInteractionEvidenceExpansionMethodShortName,
    FieldInteractionEvidenceHostOrganismScientificName,
    FieldInteractionEvidenceHostOrganismTaxId,
    FieldInteractionEvidenceHostOrganismTissue,
    FieldInteractionEvidenceIntA,
    FieldInteractionEvidenceIntABiologicalRole,
    FieldInteractionEvidenceIntASource,
    FieldInteractionEvidenceIntB,
    FieldInteractionEvidenceIntBBiologicalRole,
    FieldInteractionEvidenceIntBSource,
    FieldInteractionEvidenceInteractionDetectionMethodMiIdentifier,
    FieldInteractionEvidenceInteractionDetectionMethodShortName,
    FieldInteractionEvidenceInteractionIdentifier,
    FieldInteractionEvidenceInteractionResources,
    FieldInteractionEvidenceInteractionScore,
    FieldInteractionEvidenceInteractionTypeMiIdentifier,
    FieldInteractionEvidenceInteractionTypeShortName,
    FieldInteractionEvidenceParticipantDetectionMethodA,
    FieldInteractionEvidenceParticipantDetectionMethodB,
    FieldInteractionEvidencePubmedId,
    FieldInteractionEvidenceSpeciesA,
    FieldInteractionEvidenceSpeciesB,
    FieldInteractionEvidenceTargetA,
    FieldInteractionEvidenceTargetB,
)

node_interaction_evidence: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetInteractionEvidence),
    primary_id=FieldInteractionEvidenceInteractionIdentifier,
    label="INTERACTION_EVIDENCE",
    properties=[
        FieldInteractionEvidenceEvidenceScore,
        FieldInteractionEvidenceExpansionMethodMiIdentifier,
        FieldInteractionEvidenceExpansionMethodShortName,
        FieldInteractionEvidenceHostOrganismScientificName,
        FieldInteractionEvidenceHostOrganismTaxId,
        FieldInteractionEvidenceHostOrganismTissue,
        FieldInteractionEvidenceIntA,
        FieldInteractionEvidenceIntABiologicalRole,
        FieldInteractionEvidenceIntASource,
        FieldInteractionEvidenceIntB,
        FieldInteractionEvidenceIntBBiologicalRole,
        FieldInteractionEvidenceIntBSource,
        FieldInteractionEvidenceInteractionDetectionMethodMiIdentifier,
        FieldInteractionEvidenceInteractionDetectionMethodShortName,
        FieldInteractionEvidenceInteractionResources,
        FieldInteractionEvidenceInteractionScore,
        FieldInteractionEvidenceInteractionTypeMiIdentifier,
        FieldInteractionEvidenceInteractionTypeShortName,
        FieldInteractionEvidenceParticipantDetectionMethodA,
        FieldInteractionEvidenceParticipantDetectionMethodB,
        FieldInteractionEvidencePubmedId,
        FieldInteractionEvidenceSpeciesA,
        FieldInteractionEvidenceSpeciesB,
        FieldInteractionEvidenceTargetA,
        FieldInteractionEvidenceTargetB,
    ],
)
