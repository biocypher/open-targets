"""Summary: CELL_LINE -> BIOSAMPLE sampling relationships from CRISPR evidence.

Definition for SAMPLED_FROM edges: explodes CRISPR evidence cell line entries to
link each CELL_LINE to its anatomical BIOSAMPLE, capturing the tissue context of
assay models in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCrispr,
    FieldEvidenceCrisprDiseaseCellLines,
    FieldEvidenceCrisprDiseaseCellLinesElementId,
    FieldEvidenceCrisprDiseaseCellLinesElementTissueId,
)
from open_targets.definition.helper import get_namespaced_expression
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_cell_line_sampled_from_biosample: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidenceCrispr,
        exploded_field=FieldEvidenceCrisprDiseaseCellLines,
    ),
    primary_id=NewUuidExpression(),
    source=FieldEvidenceCrisprDiseaseCellLinesElementId,
    target=get_namespaced_expression("biosample", FieldEvidenceCrisprDiseaseCellLinesElementTissueId),
    label=EdgeLabel.SAMPLED_FROM,
    properties=[],
)
