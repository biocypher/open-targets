"""Acquisition definition that acquires 'has child' edges for molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeChildChemblIds,
    FieldMoleculeChildChemblIdsElement,
    FieldMoleculeId,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_has_child: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeChildChemblIds,
    ),
    primary_id=get_arrow_expression(FieldMoleculeId, FieldMoleculeChildChemblIdsElement),
    source=FieldMoleculeId,
    target=FieldMoleculeChildChemblIdsElement,
    label="HAS_CHILD_MOLECULE",
    properties=[],
)
