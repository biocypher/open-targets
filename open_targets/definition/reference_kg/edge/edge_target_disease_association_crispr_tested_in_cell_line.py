"""Summary: CRISPR association -> CELL_LINE tested_in edges.

Definition for TESTED_IN edges (crispr): explodes cell line entries in CRISPR
evidence to link each TARGET_DISEASE_ASSOCIATION_CRISPR node (evidence id) to the
CELL_LINE it was tested in, capturing experimental context in the KG.
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
    FieldEvidenceCrisprId,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_disease_association_crispr_tested_in_cell_line: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=ExplodingScanOperation(
            dataset=DatasetEvidenceCrispr,
            exploded_field=FieldEvidenceCrisprDiseaseCellLines,
        ),
        primary_id=NewUuidExpression(),
        source=FieldEvidenceCrisprId,
        target=FieldEvidenceCrisprDiseaseCellLinesElementId,
        label=EdgeLabel.TESTED_IN,
        properties=[],
    )
)
