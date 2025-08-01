"""Acquisition definition that acquires nodes of PMC literature entries."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidencePmcIds,
)

node_literature_entry_pmc: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidencePmcIds,
    ),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression("pmc"),
        reference=FieldExpression(FieldEvidencePmcIds.element),
    ),
    label="LITERATURE_ENTRY",
    properties=[],
)
