"""Summary: HPO phenotype terms (id/name/description) anchoring symptoms.

Definition for PHENOTYPE nodes: scans the HPO parquet to emit phenotype terms
with IDs, names, and descriptions, anchoring clinical signs/symptoms for disease
associations and mouse mapping in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetDiseaseHpo,
    FieldDiseaseHpoDescription,
    FieldDiseaseHpoId,
    FieldDiseaseHpoName,
)
from open_targets.definition.helper import get_namespaced_expression

node_phenotype: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetDiseaseHpo),
    primary_id=get_namespaced_expression("phenotype", FieldDiseaseHpoId),
    label="PHENOTYPE",
    properties=[
        FieldDiseaseHpoName,
        FieldDiseaseHpoDescription,
    ],
)
