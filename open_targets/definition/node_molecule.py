from typing import Final

from open_targets.adapter.generation_definition import (
    GenerationDefinition,
    SimpleNodeGenerationDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.data.schema import (
    FieldMoleculeBlackBoxWarning,
    FieldMoleculeCanonicalSmiles,
    FieldMoleculeChildChemblIds,
    FieldMoleculeCrossReferences,
    FieldMoleculeDescription,
    FieldMoleculeDrugType,
    FieldMoleculeHasBeenWithdrawn,
    FieldMoleculeId,
    FieldMoleculeInchiKey,
    FieldMoleculeIsApproved,
    FieldMoleculeLinkedDiseases,
    FieldMoleculeLinkedTargets,
    FieldMoleculeMaximumClinicalTrialPhase,
    FieldMoleculeName,
    FieldMoleculeParentId,
    FieldMoleculeSynonyms,
    FieldMoleculeTradeNames,
    FieldMoleculeYearOfFirstApproval,
)

node_molecule: Final[GenerationDefinition[NodeInfo]] = SimpleNodeGenerationDefinition(
    primary_id=FieldMoleculeId,
    labels=[],
    properties=[
        FieldMoleculeCanonicalSmiles,
        FieldMoleculeInchiKey,
        FieldMoleculeDrugType,
        FieldMoleculeBlackBoxWarning,
        FieldMoleculeName,
        FieldMoleculeYearOfFirstApproval,
        FieldMoleculeMaximumClinicalTrialPhase,
        FieldMoleculeParentId,
        FieldMoleculeHasBeenWithdrawn,
        FieldMoleculeIsApproved,
        FieldMoleculeTradeNames,
        FieldMoleculeSynonyms,
        FieldMoleculeCrossReferences,
        FieldMoleculeChildChemblIds,
        FieldMoleculeLinkedDiseases,
        FieldMoleculeLinkedTargets,
        FieldMoleculeDescription,
    ],
)
