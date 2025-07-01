"""Acquisition definition that acquires edges between targets and GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetKnownDrugsAggregated,
    FieldKnownDrugsAggregatedDrugId,
    FieldKnownDrugsAggregatedTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetKnownDrugsAggregated),
    primary_id=get_arrow_expression(FieldKnownDrugsAggregatedDrugId, FieldKnownDrugsAggregatedTargetId),
    source=FieldKnownDrugsAggregatedDrugId,
    target=FieldKnownDrugsAggregatedTargetId,
    label="MOLECULE_TO_TARGET_ASSOCIATION",
    properties=[],
)
