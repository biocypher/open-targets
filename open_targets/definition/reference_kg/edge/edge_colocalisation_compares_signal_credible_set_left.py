"""Summary: Edge connecting COLOCALISATION node to the left CREDIBLE_SET node.

Definition for edge: COLOCALISATION -> CREDIBLE_SET (Left side of comparison)
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import DatasetColocalisation, FieldColocalisationLeftStudyLocusId
from open_targets.definition.reference_kg.constant import EdgeLabel
from open_targets.definition.reference_kg.expression import colocalisation_primary_id_expression

edge_colocalisation_compares_signal_credible_set_left: Final[AcquisitionDefinition[EdgeInfo]] = (
    ExpressionEdgeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetColocalisation),
        primary_id=NewUuidExpression(),
        source=colocalisation_primary_id_expression,
        target=FieldColocalisationLeftStudyLocusId,
        label=EdgeLabel.COMPARES_SIGNAL,
        properties=[],
    )
)
