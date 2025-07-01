"""Acquisition definition that acquires edges between targets and diseases from AOTF Clickhouse."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetAOTFClickhouse,
    FieldAOTFClickhouseDatasourceId,
    FieldAOTFClickhouseDatatypeId,
    FieldAOTFClickhouseDiseaseData,
    FieldAOTFClickhouseDiseaseId,
    FieldAOTFClickhouseRowId,
    FieldAOTFClickhouseRowScore,
    FieldAOTFClickhouseTargetData,
    FieldAOTFClickhouseTargetId,
)
from open_targets.definition.helper import get_arrow_expression

edge_target_disease_aotf: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetAOTFClickhouse),
    primary_id=get_arrow_expression(FieldAOTFClickhouseTargetId, FieldAOTFClickhouseDiseaseId),
    source=FieldAOTFClickhouseTargetId,
    target=FieldAOTFClickhouseDiseaseId,
    label="TARGET_DISEASE_AOTF_ASSOCIATION",
    properties=[
        FieldAOTFClickhouseDatasourceId,
        FieldAOTFClickhouseDatatypeId,
        FieldAOTFClickhouseDiseaseData,
        FieldAOTFClickhouseRowId,
        FieldAOTFClickhouseRowScore,
        FieldAOTFClickhouseTargetData,
    ],
)
