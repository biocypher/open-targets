"""Acquisition definition that acquires nodes of pubmed literature entries."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceLiterature,
)

node_literature_entry_pubmed: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceLiterature,
    ),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression("pubmed"),
        reference=FieldExpression(FieldEvidenceLiterature.element),
    ),
    label="LITERATURE_ENTRY",
    properties=[],
)
