"""Acquisition definition that acquires edges from pharmacogenomics evidence to literature entries."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.data.schema import (
    DatasetPharmacogenomics,
    FieldPharmacogenomicsStudyId,
    FieldPharmacogenomicsLiterature,
)
from open_targets.definition.helper import get_arrow_expression

edge_pharmacogenomics_has_literature: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetPharmacogenomics,
        exploded_field=FieldPharmacogenomicsLiterature,
    ),
    primary_id=get_arrow_expression(
        FieldPharmacogenomicsStudyId,
        BuildCurieExpression(
            prefix=LiteralExpression("pubmed"),
            reference=FieldExpression(FieldPharmacogenomicsLiterature.element),
        ),
    ),
    source=FieldPharmacogenomicsStudyId,
    target=BuildCurieExpression(
        prefix=LiteralExpression("pubmed"),
        reference=FieldExpression(FieldPharmacogenomicsLiterature.element),
    ),
    label="HAS_LITERATURE",
    properties=[],
)
