"""Acquisition definition that acquires nodes of chemical probes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsChemicalProbes,
    FieldTargetsChemicalProbesElementControl,
    FieldTargetsChemicalProbesElementDrugId,
    FieldTargetsChemicalProbesElementId,
    FieldTargetsChemicalProbesElementIsHighQuality,
    FieldTargetsChemicalProbesElementMechanismOfAction,
    FieldTargetsChemicalProbesElementOrigin,
    FieldTargetsChemicalProbesElementProbeMinerScore,
    FieldTargetsChemicalProbesElementProbesDrugsScore,
    FieldTargetsChemicalProbesElementScoreInCells,
    FieldTargetsChemicalProbesElementScoreInOrganisms,
    FieldTargetsChemicalProbesElementTargetFromSourceId,
    FieldTargetsChemicalProbesElementUrls,
)

node_chemical_probe: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsChemicalProbes,
    ),
    primary_id=FieldTargetsChemicalProbesElementId,
    label="CHEMICAL_PROBE",
    properties=[
        FieldTargetsChemicalProbesElementControl,
        FieldTargetsChemicalProbesElementDrugId,
        FieldTargetsChemicalProbesElementIsHighQuality,
        FieldTargetsChemicalProbesElementMechanismOfAction,
        FieldTargetsChemicalProbesElementOrigin,
        FieldTargetsChemicalProbesElementProbeMinerScore,
        FieldTargetsChemicalProbesElementProbesDrugsScore,
        FieldTargetsChemicalProbesElementScoreInCells,
        FieldTargetsChemicalProbesElementScoreInOrganisms,
        FieldTargetsChemicalProbesElementTargetFromSourceId,
        FieldTargetsChemicalProbesElementUrls,
    ],
)
