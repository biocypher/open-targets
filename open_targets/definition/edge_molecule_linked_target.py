"""Acquisition definition that acquires 'linked to target' edges for molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeId,
    FieldMoleculeLinkedTargetsRows,
    FieldMoleculeLinkedTargetsRowsElement,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_linked_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeLinkedTargetsRows,
    ),
    primary_id=get_arrow_expression(FieldMoleculeId, FieldMoleculeLinkedTargetsRowsElement),
    source=FieldMoleculeId,
    target=FieldMoleculeLinkedTargetsRowsElement,
    label="LINKED_TO_TARGET",
    properties=[],
)
