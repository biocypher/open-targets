"""Acquisition definition that acquires nodes of exact disease synonyms."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesSynonymsHasExactSynonym,
    FieldDiseasesSynonymsHasExactSynonymElement,
)

node_disease_synonym_exact: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseases,
        exploded_field=FieldDiseasesSynonymsHasExactSynonym,
    ),
    primary_id=FieldDiseasesSynonymsHasExactSynonymElement,
    label="SYNONYM",
    properties=[],
)
