"""Acquisition definition that acquires nodes of URLs."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceUrls,
    FieldEvidenceUrlsElementUrl,
    FieldEvidenceUrlsElementNiceName,
)

node_url: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceUrls,
    ),
    primary_id=FieldEvidenceUrlsElementUrl,
    label="URL",
    properties=[
        FieldEvidenceUrlsElementName,
    ],
)
