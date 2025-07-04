"""Acquisition definition that acquires nodes of drug warning references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDrugWarnings,
    FieldDrugWarningsReferences,
    FieldDrugWarningsReferencesElementRefId,
    FieldDrugWarningsReferencesElementRefType,
    FieldDrugWarningsReferencesElementRefUrl,
)

node_drug_warning_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDrugWarnings,
        exploded_field=FieldDrugWarningsReferences,
    ),
    primary_id=FieldDrugWarningsReferencesElementRefId,
    label="DRUG_WARNING_REFERENCE",
    properties=[
        FieldDrugWarningsReferencesElementRefType,
        FieldDrugWarningsReferencesElementRefUrl,
    ],
)