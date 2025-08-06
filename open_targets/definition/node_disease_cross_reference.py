"""Acquisition definition that acquires nodes of disease cross references."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesDbXRefs,
    FieldDiseasesDbXRefsElement,
)

node_disease_cross_reference: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesDbXRefs,
    ),
    primary_id=FieldDiseasesDbXRefsElement,
    label="CROSS_REFERENCE",
    properties=[],
)
