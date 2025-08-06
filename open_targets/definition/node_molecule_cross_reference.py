"""Acquisition definition that acquires nodes of molecule cross references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeCrossReferences,
    FieldMoleculeCrossReferencesValueElement,
)

node_molecule_cross_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeCrossReferences,
    ),
    primary_id=FieldMoleculeCrossReferencesValueElement,
    label="CROSS_REFERENCE",
    properties=[],
)
