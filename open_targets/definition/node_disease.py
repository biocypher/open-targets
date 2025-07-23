"""Acquisition definition that acquires nodes of diseases."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetDiseases,
    FieldDiseasesCode,
    FieldDiseasesDescription,
    FieldDiseasesId,
    FieldDiseasesName,
    FieldDiseasesObsoleteTerms,
    FieldDiseasesOntologyIsTherapeuticArea,
    FieldDiseasesOntologyLeaf,
    FieldDiseasesOntologySources,
)

node_diseases: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetDiseases),
    primary_id=FieldDiseasesId,
    label="DISEASE",
    properties=[
        FieldDiseasesCode,
        FieldDiseasesDescription,
        FieldDiseasesName,
        FieldDiseasesObsoleteTerms,
        FieldDiseasesOntologyIsTherapeuticArea,
        FieldDiseasesOntologyLeaf,
        FieldDiseasesOntologySources,
    ],
)
