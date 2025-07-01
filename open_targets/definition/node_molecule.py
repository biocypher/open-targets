"""Acquisition definition that acquires nodes of molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
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

node_molecule: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMolecule),
    primary_id=FieldMoleculeId,
    label="MOLECULE",
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
