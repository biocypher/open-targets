"""Acquisition definition that acquires edges from evidence to PMC literature entries."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceId,
    FieldEvidencePmcIds,
)
from open_targets.definition.helper import get_arrow_expression

edge_evidence_has_literature_pmc: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidencePmcIds,
    ),
    primary_id=get_arrow_expression(
        FieldEvidenceId,
        BuildCurieExpression(
            prefix=LiteralExpression("pmc"),
            reference=FieldExpression(FieldEvidencePmcIdsElement),
        ),
    ),
    source=FieldEvidenceId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("pmc"),
        reference=FieldExpression(FieldEvidencePmcIdsElement),
    ),
    label="HAS_LITERATURE",
    properties=[],
)
