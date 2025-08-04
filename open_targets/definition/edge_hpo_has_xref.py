"""Acquisition definition that acquires 'has cross-reference' edges for HPO phenotypes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetHpo,
    FieldHpoDbXRefs,
    FieldHpoId,
)
from open_targets.definition.helper import get_arrow_expression

edge_hpo_has_xref: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetHpo,
        exploded_field=FieldHpoDbXRefs,
    ),
    primary_id=get_arrow_expression(FieldHpoId, FieldHpoDbXRefsElement),
    source=FieldHpoId,
    target=FieldHpoDbXRefsElement,
    label="HPO_HAS_XREF",
    properties=[],
)
