"""Acquisition definition that acquires 'linked to disease' edges for molecules."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeId,
    FieldMoleculeLinkedDiseases,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_linked_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeLinkedDiseases,
    ),
    primary_id=get_arrow_expression(FieldMoleculeId, FieldMoleculeLinkedDiseasesElement),
    source=FieldMoleculeId,
    target=FieldMoleculeLinkedDiseasesElement,
    label="LINKED_TO_DISEASE",
    properties=[],
)
