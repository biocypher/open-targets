"""Acquisition definition that acquires edges from drugs to keywords."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetSearchDrug,
    FieldSearchDrugId,
    FieldSearchDrugKeywords,
)
from open_targets.definition.helper import get_arrow_expression

edge_drug_has_keyword: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetSearchDrug,
        exploded_field=FieldSearchDrugKeywords,
    ),
    primary_id=get_arrow_expression(FieldSearchDrugId, FieldSearchDrugKeywords.element),
    source=FieldSearchDrugId,
    target=FieldSearchDrugKeywords.element,
    label="HAS_KEYWORD",
    properties=[],
)
