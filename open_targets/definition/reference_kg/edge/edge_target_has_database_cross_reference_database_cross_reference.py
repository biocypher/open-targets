"""Summary: TARGET -> DATABASE_CROSS_REFERENCE edges for target xrefs.

Definition for HAS_DATABASE_CROSS_REFERENCE edges (target): explodes target
`dbXrefs` to link each TARGET node to its DATABASE_CROSS_REFERENCE node (hashed
ID, raw value on target node), exposing external gene IDs for mapping in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTarget,
    FieldTargetDbXrefs,
    FieldTargetId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import database_cross_reference_target_primary_id_expression

edge_target_has_database_cross_reference_database_cross_reference: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetTarget,
            exploded_field=FieldTargetDbXrefs,
        ),
        primary_id=NewUuidExpression(),
        source=FieldTargetId,
        target=database_cross_reference_target_primary_id_expression,
        label=EdgeLabel.HAS_DATABASE_CROSS_REFERENCE,
        properties=[],
    )
)
