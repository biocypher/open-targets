"""Acquisition definition that acquires nodes of genetic variation biomarkers."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import BuildCurieExpression, FieldExpression, LiteralExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceBiomarkersGeneticVariation,
    FieldEvidenceBiomarkersGeneticVariationElementFunctionalConsequenceId,
    FieldEvidenceBiomarkersGeneticVariationElementId,
    FieldEvidenceBiomarkersGeneticVariationElementName,
)

node_biomarker_genetic_variation: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEvidence,
        exploded_field=FieldEvidenceBiomarkersGeneticVariation,
    ),
    primary_id=BuildCurieExpression(
        prefix=LiteralExpression("genetic_variation"),
        reference=FieldExpression(FieldEvidenceBiomarkersGeneticVariationElementId),
    ),
    label="BIOMARKER",
    properties=[
        FieldEvidenceBiomarkersGeneticVariationElementName,
        FieldEvidenceBiomarkersGeneticVariationElementFunctionalConsequenceId,
    ],
)
