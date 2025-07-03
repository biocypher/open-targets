"""Acquisition definition that acquires 'has obsolete cross-reference' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesObsoleteXRefs,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_obsolete_xref: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesObsoleteXRefs,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesObsoleteXRefs.element),
    source=FieldDiseasesId,
    target=FieldDiseasesObsoleteXRefs.element,
    label="HAS_OBSOLETE_XREF",
    properties=[],
)
