"""Acquisition definition that acquires edges from drug warnings to drug warning references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDrugWarnings,
    FieldDrugWarningsChemblIds,
    FieldDrugWarningsEfoId,
    FieldDrugWarningsReferences,
    FieldDrugWarningsReferencesElementRefId,
)
from open_targets.definition.helper import get_arrow_expression

edge_drug_warning_has_reference: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDrugWarnings,
        exploded_field=FieldDrugWarningsReferences,
    ),
    primary_id=get_arrow_expression(
        get_arrow_expression(FieldDrugWarningsChemblIds.element, FieldDrugWarningsEfoId),
        FieldDrugWarningsReferencesElementRefId,
    ),
    source=get_arrow_expression(FieldDrugWarningsChemblIds.element, FieldDrugWarningsEfoId),
    target=FieldDrugWarningsReferencesElementRefId,
    label="HAS_DRUG_WARNING_REFERENCE",
    properties=[],
)
