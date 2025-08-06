"""Acquisition definition that acquires 'has cross-reference' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesDbXRefs,
    FieldDiseasesDbXRefsElement,
    FieldDiseasesId,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_xref: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesDbXRefs,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesDbXRefsElement),
    source=FieldDiseasesId,
    target=FieldDiseasesDbXRefsElement,
    label="HAS_XREF",
    properties=[],
)
