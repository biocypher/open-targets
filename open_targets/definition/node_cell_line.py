"""Acquisition definition that acquires nodes of cell lines."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDiseaseCellLines,
    FieldEvidenceDiseaseCellLinesElementId,
    FieldEvidenceDiseaseCellLinesElementName,
    FieldEvidenceDiseaseCellLinesElementTissue,
    FieldEvidenceDiseaseCellLinesElementTissueId,
)

node_cell_line: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceDiseaseCellLines,
    ),
    primary_id=FieldEvidenceDiseaseCellLinesElementId,
    label="CELL_LINE",
    properties=[
        FieldEvidenceDiseaseCellLinesElementName,
        FieldEvidenceDiseaseCellLinesElementTissue,
        FieldEvidenceDiseaseCellLinesElementTissueId,
    ],
)
