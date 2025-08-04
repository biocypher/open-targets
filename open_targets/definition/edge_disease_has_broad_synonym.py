"""Acquisition definition that acquires 'has broad synonym' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesSynonymsHasBroadSynonym,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_broad_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasBroadSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasBroadSynonymElement),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasBroadSynonymElement,
    label="HAS_BROAD_SYNONYM",
    properties=[],
)
