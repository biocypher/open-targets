"""Acquisition definition that acquires nodes of keywords."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetLiteratureIndex,
    FieldLiteratureIndexKeywordId,
    FieldLiteratureIndexKeywordType,
)

node_keyword_literature_index: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetLiteratureIndex),
    primary_id=FieldLiteratureIndexKeywordId,
    label="KEYWORD",
    properties=[
        FieldLiteratureIndexKeywordType,
    ],
)
