"""Acquisition definition that acquires nodes of obsolete cross-references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesObsoleteXRefs,
)

node_obsolete_xref: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesObsoleteXRefs,
    ),
    primary_id=FieldDiseasesObsoleteXRefs.element,
    label="OBSOLETE_XREF",
    properties=[],
)
