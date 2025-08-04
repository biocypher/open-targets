"""Acquisition definition that acquires edges between molecules and drug warnings."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDrugWarnings,
    FieldDrugWarningsChemblIds,
    FieldDrugWarningsEfoId,
    FieldDrugWarningsEfoIdForWarningClass,
    FieldDrugWarningsEfoTerm,
    FieldDrugWarningsId,
    FieldDrugWarningsToxicityClass,
    FieldDrugWarningsWarningType,
    FieldDrugWarningsYear,
)
from open_targets.definition.helper import get_arrow_expression

edge_molecule_drug_warning: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDrugWarnings,
        exploded_field=FieldDrugWarningsChemblIds,
    ),
    primary_id=get_arrow_expression(FieldDrugWarningsChemblIdsElement, FieldDrugWarningsEfoId),
    source=FieldDrugWarningsChemblIdsElement,
    target=FieldDrugWarningsEfoId,
    label="MOLECULE_TO_DRUG_WARNING",
    properties=[
        FieldDrugWarningsEfoIdForWarningClass,
        FieldDrugWarningsEfoTerm,
        FieldDrugWarningsId,
        FieldDrugWarningsToxicityClass,
        FieldDrugWarningsWarningType,
        FieldDrugWarningsYear,
        FieldDrugWarningsCountry,
        FieldDrugWarningsDescription,
        FieldDrugWarningsReferences,
    ],
)
