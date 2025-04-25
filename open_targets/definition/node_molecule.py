"""Acquisition definition that acquires nodes of molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
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
from open_targets.definition.curie_prefix import CHEMBL_PREFIX
from open_targets.definition.node_shared import node_static_properties

node_molecule: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMolecule),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression(CHEMBL_PREFIX),
        reference=FieldExpression(FieldMoleculeId),
        normalise=True,
    ),
    label=CHEMBL_PREFIX,
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
        *node_static_properties,
    ],
)
