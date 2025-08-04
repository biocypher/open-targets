"""Acquisition definition that acquires 'is a' edges between HPO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetHpo,
    FieldHpoId,
    FieldHpoParents,
)
from open_targets.definition.helper import get_arrow_expression

edge_hpo_term_is_a: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetHpo,
        exploded_field=FieldHpoParents,
    ),
    primary_id=get_arrow_expression(FieldHpoId, FieldHpoParentsElement),
    source=FieldHpoId,
    target=FieldHpoParentsElement,
    label="HPO_TERM_IS_A",
    properties=[],
)
