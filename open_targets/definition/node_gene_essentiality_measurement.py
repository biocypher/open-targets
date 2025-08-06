"""Acquisition definition that acquires nodes of gene essentiality measurements."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargetEssentiality,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreens,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementCellLineName,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDepmapId,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDiseaseCellLineId,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDiseaseFromSource,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementExpression,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementGeneEffect,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementMutation,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementTissueId,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementTissueName,
    FieldTargetEssentialityGeneEssentialityElementIsEssential,
    FieldTargetEssentialityId,
)
from open_targets.definition.helper import get_arrow_expression

node_gene_essentiality_measurement: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargetEssentiality,
        exploded_field=FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreens,
    ),
    primary_id=get_arrow_expression(
        FieldTargetEssentialityId,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDepmapId,
    ),
    label="GENE_ESSENTIALITY_MEASUREMENT",
    properties=[
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementCellLineName,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDiseaseCellLineId,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDiseaseFromSource,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementExpression,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementGeneEffect,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementMutation,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementTissueId,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementTissueName,
        FieldTargetEssentialityGeneEssentialityElementIsEssential,
    ],
)
