"""Acquisition definition that acquires nodes of obsolete cross-references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesObsoleteTerms,
)

node_obsolete_term: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesObsoleteTerms,
    ),
    primary_id=FieldDiseasesObsoleteTerms.element,
    label="OBSOLETE_TERM",
    properties=[],
)
