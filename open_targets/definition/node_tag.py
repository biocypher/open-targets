"""Acquisition definition that acquires nodes of tags."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetEpmcCooccurrences,
    FieldEpmcCooccurrencesAnns,
    FieldEpmcCooccurrencesAnnsElementTags,
    FieldEpmcCooccurrencesAnnsElementTagsElementName,
    FieldEpmcCooccurrencesAnnsElementTagsElementUri,
)

node_tag: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetEpmcCooccurrences,
        exploded_field=FieldEpmcCooccurrencesAnnsElementTags,
    ),
    primary_id=FieldEpmcCooccurrencesAnnsElementTagsElementName,
    label="TAG",
    properties=[
        FieldEpmcCooccurrencesAnnsElementTagsElementUri,
    ],
)
