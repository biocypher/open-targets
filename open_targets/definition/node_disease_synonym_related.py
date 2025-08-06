"""Acquisition definition that acquires nodes of related disease synonyms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesSynonymsHasRelatedSynonym,
    FieldDiseasesSynonymsHasRelatedSynonymElement,
)

node_disease_synonym_related: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasRelatedSynonym,
    ),
    primary_id=FieldDiseasesSynonymsHasRelatedSynonymElement,
    label="SYNONYM",
    properties=[],
)
