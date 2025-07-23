"""Acquisition definition that acquires nodes of drug responses."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidence,
    FieldEvidenceDrugResponse,
)
from open_targets.definition.helper import get_arrow_expression

node_drug_response: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidence),
    primary_id=get_arrow_expression(FieldEvidenceDrugResponse.f_drug_id, FieldEvidenceDrugResponse.f_response),
    label="DRUG_RESPONSE",
    properties=[
        FieldEvidenceDrugResponse.f_drug_name,
        FieldEvidenceDrugResponse.f_response,
    ],
)
