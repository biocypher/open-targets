"""Summary: ChEMBL molecule entities (drug metadata, modality, approval state).

Definition for MOLECULE nodes: scans the Molecule parquet (ChEMBL subset) to emit
drug entities with modality, approval/withdrawn status, trade names, synonyms,
description, max clinical phase, and structure IDs as the drug anchor for
indications, mechanisms of action, warnings, and ADR edges in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetDrugMolecule,
    FieldDrugMoleculeBlackBoxWarning,
    FieldDrugMoleculeDescription,
    FieldDrugMoleculeDrugType,
    FieldDrugMoleculeHasBeenWithdrawn,
    FieldDrugMoleculeId,
    FieldDrugMoleculeInchiKey,
    FieldDrugMoleculeIsApproved,
    FieldDrugMoleculeMaximumClinicalTrialPhase,
    FieldDrugMoleculeName,
    FieldDrugMoleculeSynonyms,
    FieldDrugMoleculeTradeNames,
    FieldDrugMoleculeYearOfFirstApproval,
)
from open_targets.definition.helper import get_null_if_empty_list_expression

node_molecule: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetDrugMolecule),
    primary_id=FieldDrugMoleculeId,
    label="MOLECULE",
    properties=[
        FieldDrugMoleculeInchiKey,
        FieldDrugMoleculeDrugType,
        FieldDrugMoleculeBlackBoxWarning,
        FieldDrugMoleculeName,
        FieldDrugMoleculeYearOfFirstApproval,
        FieldDrugMoleculeMaximumClinicalTrialPhase,
        FieldDrugMoleculeHasBeenWithdrawn,
        FieldDrugMoleculeIsApproved,
        (FieldDrugMoleculeTradeNames.name, get_null_if_empty_list_expression(FieldDrugMoleculeTradeNames)),
        (FieldDrugMoleculeSynonyms.name, get_null_if_empty_list_expression(FieldDrugMoleculeSynonyms)),
        FieldDrugMoleculeDescription,
    ],
)
