"""Acquisition definition that acquires edges from targets to chemical probes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsChemicalProbes,
    FieldTargetsChemicalProbesElementId,
    FieldTargetsId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_chemical_probe: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsChemicalProbes,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsChemicalProbesElementId),
    source=FieldTargetsId,
    target=FieldTargetsChemicalProbesElementId,
    label="HAS_CHEMICAL_PROBE",
    properties=[],
)
