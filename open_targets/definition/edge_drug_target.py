"""Acquisition definition that acquires edges between drugs (molecules) and genes (targets) using the known drug dataset."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.expression import (
    BuildCurieExpression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
)
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeId,
    FieldMoleculeLinkedTargetsRows,
    FieldMoleculeLinkedTargetsRowsElement,
)
from open_targets.definition.curie_prefix import CHEMBL_PREFIX, ENSEMBL_PREFIX
from open_targets.definition.node_shared import node_static_properties

edge_drug_target: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeLinkedTargetsRows,
    ),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(CHEMBL_PREFIX),
                reference=FieldExpression(FieldMoleculeId),
                normalise=True,
            ),
            LiteralExpression("->"),
            BuildCurieExpression(
                prefix=LiteralExpression(ENSEMBL_PREFIX),
                reference=FieldExpression(FieldMoleculeLinkedTargetsRowsElement),
                normalise=True,
            ),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(CHEMBL_PREFIX),
        reference=FieldExpression(FieldMoleculeId),
        normalise=True,
    ),
    target=BuildCurieExpression(
        prefix=LiteralExpression(ENSEMBL_PREFIX),
        reference=FieldExpression(FieldMoleculeLinkedTargetsRowsElement),
        normalise=True,
    ),
    label=LiteralExpression("DRUG_TO_GENE_ASSOCIATION"),
    properties=node_static_properties,
)
