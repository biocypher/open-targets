"""Acquisition definition that acquires edges from pharmacogenomics evidence to variants."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetPharmacogenomics,
    FieldPharmacogenomicsStudyId,
    FieldPharmacogenomicsVariantRsId,
)
from open_targets.definition.helper import get_arrow_expression

edge_pharmacogenomics_about_variant: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetPharmacogenomics),
    primary_id=get_arrow_expression(FieldPharmacogenomicsStudyId, FieldPharmacogenomicsVariantRsId),
    source=FieldPharmacogenomicsStudyId,
    target=FieldPharmacogenomicsVariantRsId,
    label="ABOUT_VARIANT",
    properties=[],
)