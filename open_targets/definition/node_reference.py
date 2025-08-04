"""Acquisition definition that acquires nodes of references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseaseToPhenotype,
    FieldDiseaseToPhenotypeEvidenceElementReferences,
)

node_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseaseToPhenotype,
        exploded_field=FieldDiseaseToPhenotypeEvidenceElementReferences,
    ),
    primary_id=FieldDiseaseToPhenotypeEvidenceElementReferencesElement,
    label="REFERENCE",
    properties=[],
)
