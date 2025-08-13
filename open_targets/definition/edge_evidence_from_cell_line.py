"""Acquisition definition that acquires edges from evidence to cell lines."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDiseaseCellLines,
    FieldEvidenceDiseaseCellLinesElementId,
    FieldEvidenceId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_from_cell_line: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceDiseaseCellLines,
    ),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceDiseaseCellLinesElementId),
    source=FieldEvidenceId,
    target=FieldEvidenceDiseaseCellLinesElementId,
    label="FROM_CELL_LINE",
    properties=[],
)
