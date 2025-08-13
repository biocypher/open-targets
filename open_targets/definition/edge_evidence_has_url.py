"""Acquisition definition that acquires edges from evidence to URLs."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidenceUrls,
    FieldEvidenceUrlsElementUrl,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_url: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceUrls,
    ),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidenceUrlsElementUrl),
    source=FieldEvidenceId,
    target=FieldEvidenceUrlsElementUrl,
    label="HAS_URL",
    properties=[],
)
