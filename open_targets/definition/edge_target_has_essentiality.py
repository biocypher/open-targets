"""Acquisition definition that acquires edges from targets to gene essentiality measurements."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetTargetEssentiality,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreens,
    FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDepmapId,
    FieldTargetEssentialityId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_has_essentiality: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetTargetEssentiality,
        exploded_field=FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreens,
    ),
    primary_id=get_arrow_expression(
        FieldTargetEssentialityId,
        get_arrow_expression(
            FieldTargetEssentialityId,
            FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDepmapId,
        ),
    ),
    source=FieldTargetEssentialityId,
    target=get_arrow_expression(
        FieldTargetEssentialityId,
        FieldTargetEssentialityGeneEssentialityElementDepMapEssentialityElementScreensElementDepmapId,
    ),
    label="HAS_ESSENTIALITY",
    properties=[],
)
