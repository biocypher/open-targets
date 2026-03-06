"""Summary: TARGET -> BIOSAMPLE expression edges.

Definition for EXPRESSED_IN edges
(target -> biosample): explodes the tissues array
in the expression dataset to link each TARGET to
the BIOSAMPLE where it is expressed, carrying RNA
and protein expression levels.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionEdgeAcquisitionDefinition,
)
from open_targets.adapter.expression import NewUuidExpression
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetExpression,
    FieldExpressionId,
    FieldExpressionTissues,
    FieldExpressionTissuesElementEfoCode,
    FieldExpressionTissuesElementLabel,
    FieldExpressionTissuesElementProtein,
    FieldExpressionTissuesElementProteinLevel,
    FieldExpressionTissuesElementProteinReliability,
    FieldExpressionTissuesElementRna,
    FieldExpressionTissuesElementRnaLevel,
    FieldExpressionTissuesElementRnaUnit,
    FieldExpressionTissuesElementRnaValue,
    FieldExpressionTissuesElementRnaZscore,
)
from open_targets.definition.reference_kg.constant import EdgeLabel

edge_target_expressed_in_biosample: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetExpression,
        exploded_field=FieldExpressionTissues,
    ),
    primary_id=NewUuidExpression(),
    source=FieldExpressionId,
    target=FieldExpressionTissuesElementEfoCode,
    label=EdgeLabel.EXPRESSED_IN,
    properties=[
        FieldExpressionTissuesElementLabel,
        (
            f"{FieldExpressionTissuesElementRna.name}_{FieldExpressionTissuesElementRnaValue.name}",
            FieldExpressionTissuesElementRnaValue,
        ),
        (
            f"{FieldExpressionTissuesElementRna.name}_{FieldExpressionTissuesElementRnaZscore.name}",
            FieldExpressionTissuesElementRnaZscore,
        ),
        (
            f"{FieldExpressionTissuesElementRna.name}_{FieldExpressionTissuesElementRnaLevel.name}",
            FieldExpressionTissuesElementRnaLevel,
        ),
        (
            f"{FieldExpressionTissuesElementRna.name}_{FieldExpressionTissuesElementRnaUnit.name}",
            FieldExpressionTissuesElementRnaUnit,
        ),
        (
            f"{FieldExpressionTissuesElementProtein.name}_{FieldExpressionTissuesElementProteinReliability.name}",
            FieldExpressionTissuesElementProteinReliability,
        ),
        (
            f"{FieldExpressionTissuesElementProtein.name}_{FieldExpressionTissuesElementProteinLevel.name}",
            FieldExpressionTissuesElementProteinLevel,
        ),
    ],
)
