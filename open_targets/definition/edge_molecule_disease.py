"""Acquisition definition that acquires edges between targets and GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
    ToStringExpression,
)
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetKnownDrugsAggregated,
    FieldKnownDrugsAggregatedDiseaseId,
    FieldKnownDrugsAggregatedDrugId,
)
from open_targets.definition.curie_prefix import CHEMBL_PREFIX

edge_molecule_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetKnownDrugsAggregated),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(CHEMBL_PREFIX),
                reference=FieldExpression(FieldKnownDrugsAggregatedDrugId),
                normalise=True,
            ),
            LiteralExpression("->"),
            NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldKnownDrugsAggregatedDiseaseId))),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(CHEMBL_PREFIX),
        reference=FieldExpression(FieldKnownDrugsAggregatedDrugId),
        normalise=True,
    ),
    target=NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldKnownDrugsAggregatedDiseaseId))),
    label=LiteralExpression("DRUG_TO_DISEASE_ASSOCIATION"),
    properties=[],
)
