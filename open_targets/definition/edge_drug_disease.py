"""Acquisition definition that acquires edges between drugs (molecules) and diseases using linkedDiseases."""

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
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetMolecule,
    FieldMoleculeId,
    FieldMoleculeLinkedDiseasesRows,
    FieldMoleculeLinkedDiseasesRowsElement,
)
from open_targets.definition.curie_prefix import CHEMBL_PREFIX
from open_targets.definition.node_shared import node_static_properties

edge_drug_disease: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetMolecule,
        exploded_field=FieldMoleculeLinkedDiseasesRows,
    ),
    primary_id=StringConcatenationExpression(
        expressions=[
            BuildCurieExpression(
                prefix=LiteralExpression(CHEMBL_PREFIX),
                reference=FieldExpression(FieldMoleculeId),
                normalise=True,
            ),
            LiteralExpression("->"),
            NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldMoleculeLinkedDiseasesRowsElement))),
        ],
    ),
    source=BuildCurieExpression(
        prefix=LiteralExpression(CHEMBL_PREFIX),
        reference=FieldExpression(FieldMoleculeId),
        normalise=True,
    ),
    target=NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldMoleculeLinkedDiseasesRowsElement))),
    label=LiteralExpression("DRUG_TO_DISEASE_ASSOCIATION"),
    properties=node_static_properties,
)
