"""Acquisition definition that acquires edges between mouse targets and human targets."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetMousePhenotypes,
    FieldMousePhenotypesTargetInModelEnsemblId,
    FieldMousePhenotypesTargetFromSourceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_mouse_target_models_human_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetMousePhenotypes),
    primary_id=get_arrow_expression(FieldMousePhenotypesTargetInModelEnsemblId, FieldMousePhenotypesTargetFromSourceId),
    source=FieldMousePhenotypesTargetInModelEnsemblId,
    target=FieldMousePhenotypesTargetFromSourceId,
    label="MODELS_HUMAN_TARGET",
    properties=[],
)
