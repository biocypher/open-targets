"""Acquisition definition that acquires nodes of variant effects."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetVariant,
    FieldVariantVariantEffect,
    FieldVariantVariantEffectElementMethod,
    FieldVariantVariantEffectElementAssessment,
    FieldVariantVariantEffectElementScore,
    FieldVariantVariantEffectElementAssessmentFlag,
    FieldVariantVariantEffectElementTargetId,
    FieldVariantVariantEffectElementNormalisedScore,
)
from open_targets.definition.helper import get_arrow_expression

node_variant_effect: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetVariant,
        exploded_field=FieldVariantVariantEffect,
    ),
    primary_id=get_arrow_expression(
        FieldVariantVariantEffectElementTargetId,
        FieldVariantVariantEffectElementMethod,
    ),
    label="VARIANT_EFFECT",
    properties=[
        FieldVariantVariantEffectElementAssessment,
        FieldVariantVariantEffectElementScore,
        FieldVariantVariantEffectElementAssessmentFlag,
        FieldVariantVariantEffectElementNormalisedScore,
    ],
)
