"""Acquisition definition that acquires nodes of annotations."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementExact,
    FieldEpmcCooccurrencesAnnsElementSection,
    FieldEpmcCooccurrencesAnnsElementType,
)

node_annotation: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnns,
    ),
    primary_id=FieldEpmcCooccurrencesAnnsElementExact,
    label="ANNOTATION",
    properties=[
        FieldEpmcCooccurrencesAnnsElementSection,
        FieldEpmcCooccurrencesAnnsElementType,
    ],
)
