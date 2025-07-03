"""Acquisition definition that acquires edges between literature entries and keywords."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetLiteratureIndex,
    FieldLiteratureIndexPmid,
    FieldLiteratureIndexKeywordId,
    FieldLiteratureIndexKeywordType,
)
from open_targets.definition.helper import get_arrow_expression

edge_literature_mentions_keyword: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetLiteratureIndex),
    primary_id=get_arrow_expression(FieldLiteratureIndexPmid, FieldLiteratureIndexKeywordId),
    source=FieldLiteratureIndexPmid,
    target=FieldLiteratureIndexKeywordId,
    label="MENTIONS_KEYWORD",
    properties=[
        FieldLiteratureIndexKeywordType,
    ],
)
