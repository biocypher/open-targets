"""Acquisition definition that acquires edges from evidence to pathways."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidencePathways,
    FieldEvidencePathwaysElementId,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_pathway: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidencePathways,
    ),
    primary_id=get_arrow_expression(FieldEvidenceId, FieldEvidencePathwaysElementId),
    source=FieldEvidenceId,
    target=FieldEvidencePathwaysElementId,
    label="HAS_PATHWAY",
    properties=[],
)
