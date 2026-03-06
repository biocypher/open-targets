"""Summary: target prioritisation factor nodes.

Definition for TARGET_PRIORITISATION nodes: scans
the target_prioritisation parquet to emit
target-specific scoring records from the Target
Engine project, carrying tractability flags
(hasPocket, hasLigand, isInMembrane, isSecreted),
safety signals (hasSafetyEvent, geneticConstraint),
development status (maxClinicalTrialPhase), and
other druggability and conservation metrics as
prioritisation evidence in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetTargetPrioritisation,
    FieldTargetPrioritisationGeneticConstraint,
    FieldTargetPrioritisationHasHighQualityChemicalProbes,
    FieldTargetPrioritisationHasLigand,
    FieldTargetPrioritisationHasPocket,
    FieldTargetPrioritisationHasSafetyEvent,
    FieldTargetPrioritisationHasSmallMoleculeBinder,
    FieldTargetPrioritisationHasTep,
    FieldTargetPrioritisationIsCancerDriverGene,
    FieldTargetPrioritisationIsInMembrane,
    FieldTargetPrioritisationIsSecreted,
    FieldTargetPrioritisationMaxClinicalTrialPhase,
    FieldTargetPrioritisationMouseKoScore,
    FieldTargetPrioritisationMouseOrthologMaxIdentityPercentage,
    FieldTargetPrioritisationParalogMaxIdentityPercentage,
    FieldTargetPrioritisationTissueDistribution,
    FieldTargetPrioritisationTissueSpecificity,
)
from open_targets.definition.reference_kg.expression import (
    target_prioritisation_primary_id_expression,
)

node_target_prioritisation: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargetPrioritisation),
    primary_id=target_prioritisation_primary_id_expression,
    label="TARGET_PRIORITISATION",
    properties=[
        FieldTargetPrioritisationIsInMembrane,
        FieldTargetPrioritisationIsSecreted,
        FieldTargetPrioritisationHasSafetyEvent,
        FieldTargetPrioritisationHasPocket,
        FieldTargetPrioritisationHasLigand,
        FieldTargetPrioritisationHasSmallMoleculeBinder,
        FieldTargetPrioritisationGeneticConstraint,
        FieldTargetPrioritisationParalogMaxIdentityPercentage,
        FieldTargetPrioritisationMouseOrthologMaxIdentityPercentage,
        FieldTargetPrioritisationIsCancerDriverGene,
        FieldTargetPrioritisationHasTep,
        FieldTargetPrioritisationMouseKoScore,
        FieldTargetPrioritisationHasHighQualityChemicalProbes,
        FieldTargetPrioritisationMaxClinicalTrialPhase,
        FieldTargetPrioritisationTissueSpecificity,
        FieldTargetPrioritisationTissueDistribution,
    ],
)
