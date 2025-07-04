"""Acquisition definition that acquires edges from targets to protein identifiers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargets,
    FieldTargetsId,
    FieldTargetsProteinIds,
    FieldTargetsProteinIdsElementId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_protein_id: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargets,
        exploded_field=FieldTargetsProteinIds,
    ),
    primary_id=get_arrow_expression(FieldTargetsId, FieldTargetsProteinIdsElementId),
    source=FieldTargetsId,
    target=FieldTargetsProteinIdsElementId,
    label="HAS_PROTEIN_ID",
    properties=[],
)
