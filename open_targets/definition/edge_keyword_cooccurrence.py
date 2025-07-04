"""Acquisition definition that acquires edges between co-occurring keywords."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetCooccurrences,
    FieldCooccurrencesDate,
    FieldCooccurrencesDay,
    FieldCooccurrencesEnd1,
    FieldCooccurrencesEnd2,
    FieldCooccurrencesEvidenceScore,
    FieldCooccurrencesIsMapped,
    FieldCooccurrencesKeywordId1,
    FieldCooccurrencesKeywordId2,
    FieldCooccurrencesLabel1,
    FieldCooccurrencesLabel2,
    FieldCooccurrencesLabelN1,
    FieldCooccurrencesLabelN2,
    FieldCooccurrencesMonth,
    FieldCooccurrencesOrganisms,
    FieldCooccurrencesPmcid,
    FieldCooccurrencesPmid,
    FieldCooccurrencesPubDate,
    FieldCooccurrencesSection,
    FieldCooccurrencesStart1,
    FieldCooccurrencesStart2,
    FieldCooccurrencesText,
    FieldCooccurrencesTraceSource,
    FieldCooccurrencesType,
    FieldCooccurrencesType1,
    FieldCooccurrencesType2,
    FieldCooccurrencesYear,
)
from open_targets.definition.helper import get_arrow_expression

edge_keyword_cooccurrence: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetCooccurrences),
    primary_id=get_arrow_expression(FieldCooccurrencesKeywordId1, FieldCooccurrencesKeywordId2),
    source=FieldCooccurrencesKeywordId1,
    target=FieldCooccurrencesKeywordId2,
    label="KEYWORD_COOCCURRENCE",
    properties=[
        FieldCooccurrencesDate,
        FieldCooccurrencesDay,
        FieldCooccurrencesEnd1,
        FieldCooccurrencesEnd2,
        FieldCooccurrencesEvidenceScore,
        FieldCooccurrencesIsMapped,
        FieldCooccurrencesLabel1,
        FieldCooccurrencesLabel2,
        FieldCooccurrencesLabelN1,
        FieldCooccurrencesLabelN2,
        FieldCooccurrencesMonth,
        FieldCooccurrencesOrganisms,
        FieldCooccurrencesPmcid,
        FieldCooccurrencesPmid,
        FieldCooccurrencesPubDate,
        FieldCooccurrencesSection,
        FieldCooccurrencesStart1,
        FieldCooccurrencesStart2,
        FieldCooccurrencesText,
        FieldCooccurrencesTraceSource,
        FieldCooccurrencesType,
        FieldCooccurrencesType1,
        FieldCooccurrencesType2,
        FieldCooccurrencesYear,
    ],
)
