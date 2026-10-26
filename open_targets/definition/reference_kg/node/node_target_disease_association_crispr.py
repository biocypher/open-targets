"""Summary: CRISPR perturbation screens linking targets to disease phenotypes.

Definition for TARGET_DISEASE_ASSOCIATION_CRISPR nodes: filters Evidence
parquet to crispr source to emit CRISPR functional screen associations. CRISPR
perturbs genes in disease-relevant cell lines; if knocking out a gene changes a
phenotype linked to the disease, the gene is implicated. Records keep disease
IDs, target IDs/symbols, and resource/overall scores; cell-line context is
represented by the exploded TESTED_IN edges. The inference is perturb
gene → observe phenotype change → link gene to disease in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceCrispr,
    FieldEvidenceCrisprDiseaseFromSource,
    FieldEvidenceCrisprDiseaseFromSourceMappedId,
    FieldEvidenceCrisprId,
    FieldEvidenceCrisprResourceScore,
    FieldEvidenceCrisprScore,
    FieldEvidenceCrisprTargetFromSourceId,
)

node_target_disease_association_crispr: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetEvidenceCrispr),
    primary_id=FieldEvidenceCrisprId,
    label="TARGET_DISEASE_ASSOCIATION_CRISPR",
    properties=[
        FieldEvidenceCrisprDiseaseFromSource,
        FieldEvidenceCrisprDiseaseFromSourceMappedId,
        FieldEvidenceCrisprResourceScore,
        FieldEvidenceCrisprScore,
        FieldEvidenceCrisprTargetFromSourceId,
    ],
)
