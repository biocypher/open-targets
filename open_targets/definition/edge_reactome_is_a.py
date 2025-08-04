"""Acquisition definition that acquires 'is a' edges between Reactome pathways."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetReactome,
    FieldReactomeId,
    FieldReactomeParents,
)
from open_targets.definition.helper import get_arrow_expression

edge_reactome_is_a: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetReactome,
        exploded_field=FieldReactomeParents,
    ),
    primary_id=get_arrow_expression(FieldReactomeId, FieldReactomeParentsElement),
    source=FieldReactomeId,
    target=FieldReactomeParentsElement,
    label="REACTOME_IS_A",
    properties=[],
)
