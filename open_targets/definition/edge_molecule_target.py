"""Acquisition definition that acquires edges between targets and GO terms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
)
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetKnownDrugsAggregated,
    FieldKnownDrugsAggregatedDrugId,
    FieldKnownDrugsAggregatedTargetId,
)
from open_targets.definition.curie_prefix import CHEMBL_PREFIX, ENSEMBL_PREFIX

edge_molecule_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetKnownDrugsAggregated),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(CHEMBL_PREFIX),
                reference=FieldExpression(FieldKnownDrugsAggregatedDrugId),
                normalise=True,
            ),
            LiteralExpression("->"),
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_PREFIX),
                reference=FieldExpression(FieldKnownDrugsAggregatedTargetId),
                normalise=True,
            ),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(CHEMBL_PREFIX),
        reference=FieldExpression(FieldKnownDrugsAggregatedDrugId),
        normalise=True,
    ),
    target=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldKnownDrugsAggregatedTargetId),
        normalise=True,
    ),
    label=LiteralExpression("DRUG_TO_GENE_ASSOCIATION"),
    properties=[],
)
