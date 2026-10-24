"""Summary: BIOSAMPLE hierarchy IS_A edges (child -> parent).

Definition for IS_A edges (biosample hierarchy): explodes parent relationships
in the biosample parquet to link each BIOSAMPLE node to its parent BIOSAMPLE,
forming the ontology hierarchy in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetBiosample,
    FieldBiosampleBiosampleId,
    FieldBiosampleParents,
    FieldBiosampleParentsElement,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_biosample_is_a_biosample: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetBiosample,
        exploded_field=FieldBiosampleParents,
    ),
    primary_id=NewUuidExpression(),
    source=FieldBiosampleBiosampleId,
    target=FieldBiosampleParentsElement,
    label=EdgeLabel.IS_A,
    properties=[],
)
