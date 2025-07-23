"""Acquisition definition that acquires nodes of cross-references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesDbXRefs,
    DatasetMolecule,
    FieldMoleculeCrossReferences,
)

node_disease_cross_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesDbXRefs,
    ),
    primary_id=FieldDiseasesDbXRefs.element,
    label="CROSS_REFERENCE",
    properties=[],
)

node_molecule_cross_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeCrossReferences,
    ),
    primary_id=FieldMoleculeCrossReferences.value.element,
    label="CROSS_REFERENCE",
    properties=[],
)
