"""Acquisition definition that acquires 'has synonym' edges for diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesId,
    FieldDiseasesSynonymsHasBroadSynonym,
    FieldDiseasesSynonymsHasExactSynonym,
    FieldDiseasesSynonymsHasNarrowSynonym,
    FieldDiseasesSynonymsHasRelatedSynonym,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_has_broad_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasBroadSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasBroadSynonym.element),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasBroadSynonym.element,
    label="HAS_BROAD_SYNONYM",
    properties=[],
)

edge_disease_has_exact_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasExactSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasExactSynonym.element),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasExactSynonym.element,
    label="HAS_EXACT_SYNONYM",
    properties=[],
)

edge_disease_has_narrow_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasNarrowSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasNarrowSynonym.element),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasNarrowSynonym.element,
    label="HAS_NARROW_SYNONYM",
    properties=[],
)

edge_disease_has_related_synonym: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasRelatedSynonym,
    ),
    primary_id=get_arrow_expression(FieldDiseasesId, FieldDiseasesSynonymsHasRelatedSynonym.element),
    source=FieldDiseasesId,
    target=FieldDiseasesSynonymsHasRelatedSynonym.element,
    label="HAS_RELATED_SYNONYM",
    properties=[],
)
