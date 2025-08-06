"""Acquisition definition that acquires 'has exact synonym' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesSynonymsHasExactSynonym,
    FieldDiseasesSynonymsHasExactSynonymElement,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_exact_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasExactSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasExactSynonymElement),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasExactSynonymElement,
    label="HAS_EXACT_SYNONYM",
    properties=[],
)
