"""Acquisition definition that acquires 'is a' edges between HPO phenotypes."""

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

edge_hpo_is_a: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetHpo,
        exploded_field=FieldHpoParents,
    ),
    primary_id=get_arrow_expression(FieldHpoId, FieldHpoParents.element),
    source=FieldHpoId,
    target=FieldHpoParents.element,
    label="HPO_IS_A",
    properties=[],
)
