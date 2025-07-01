"""Acquisition definition that acquires edges between targets and diseases from Ebisearch Associations."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEbisearchAssociations,
    FieldEbisearchAssociationsApprovedSymbol,
    FieldEbisearchAssociationsDiseaseId,
    FieldEbisearchAssociationsName,
    FieldEbisearchAssociationsScore,
    FieldEbisearchAssociationsTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_ebisearch: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEbisearchAssociations),
    primary_id=get_arrow_expression(FieldEbisearchAssociationsTargetId, FieldEbisearchAssociationsDiseaseId),
    source=FieldEbisearchAssociationsTargetId,
    target=FieldEbisearchAssociationsDiseaseId,
    label="TARGET_TO_DISEASE_ASSOCIATION_EBISearch",
    properties=[
        FieldEbisearchAssociationsApprovedSymbol,
        FieldEbisearchAssociationsName,
        FieldEbisearchAssociationsScore,
    ],
)
