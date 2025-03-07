from typing import Final

from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.generation_definition import (
    ExpressionNodeGenerationDefinition,
    GenerationDefinition,
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
from open_targets.definition.node_shared import node_static_properties

_TYPE: Final = "chembl"

node_molecule: Final[GenerationDefinition[NodeInfo]] = ExpressionNodeGenerationDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMolecule),
    primary_id=BuildCurieExpression(
        scheme=LiteralExpression(_TYPE),
        path=FieldExpression(FieldMoleculeId),
        normalised=True,
    ),
    labels=[_TYPE],
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
