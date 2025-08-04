"""Acquisition definition that acquires 'has synonym' edges for molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeId,
    FieldMoleculeSynonyms,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_has_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeSynonyms,
    ),
    primary_id=get_arrow_expression(FieldMoleculeId, FieldMoleculeSynonymsElement),
    source=FieldMoleculeId,
    target=FieldMoleculeSynonymsElement,
    label="HAS_SYNONYM",
    properties=[],
)
