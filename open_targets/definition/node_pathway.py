"""Acquisition definition that acquires nodes of pathways."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidencePathways,
    FieldEvidencePathwaysElementId,
    FieldEvidencePathwaysElementName,
)

node_pathway: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidencePathways,
    ),
    primary_id=FieldEvidencePathwaysElementId,
    label="PATHWAY",
    properties=[
        FieldEvidencePathwaysElementName,
    ],
)
