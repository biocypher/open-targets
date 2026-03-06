"""Summary: pharmacogenomics clinical annotations.

Definition for PHARMACOGENOMICS_ANNOTATION nodes:
scans the pharmacogenomics parquet to emit clinical
annotation records linking genetic variants to drug
responses, carrying genotype, evidence level,
directionality, phenotype text, PGx category,
haplotype, and functional consequence details as
the pharmacogenomics annotation nodes in the KG.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import (
    AcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetPharmacogenomics,
    FieldPharmacogenomicsDatasourceId,
    FieldPharmacogenomicsDatasourceVersion,
    FieldPharmacogenomicsDatatypeId,
    FieldPharmacogenomicsDirectionality,
    FieldPharmacogenomicsEvidenceLevel,
    FieldPharmacogenomicsGenotype,
    FieldPharmacogenomicsGenotypeAnnotationText,
    FieldPharmacogenomicsGenotypeId,
    FieldPharmacogenomicsHaplotypeFromSourceId,
    FieldPharmacogenomicsHaplotypeId,
    FieldPharmacogenomicsIsDirectTarget,
    FieldPharmacogenomicsPgxCategory,
    FieldPharmacogenomicsPhenotypeFromSourceId,
    FieldPharmacogenomicsPhenotypeText,
    FieldPharmacogenomicsTargetFromSourceId,
    FieldPharmacogenomicsVariantFunctionalConsequenceId,
    FieldPharmacogenomicsVariantId,
    FieldPharmacogenomicsVariantRsId,
)
from open_targets.definition.reference_kg.expression import (
    pharmacogenomics_annotation_primary_id_expression,
)

node_pharmacogenomics_annotation: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetPharmacogenomics),
    primary_id=pharmacogenomics_annotation_primary_id_expression,
    label="PHARMACOGENOMICS_ANNOTATION",
    properties=[
        FieldPharmacogenomicsDatasourceId,
        FieldPharmacogenomicsDatasourceVersion,
        FieldPharmacogenomicsDatatypeId,
        FieldPharmacogenomicsDirectionality,
        FieldPharmacogenomicsEvidenceLevel,
        FieldPharmacogenomicsGenotype,
        FieldPharmacogenomicsGenotypeAnnotationText,
        FieldPharmacogenomicsGenotypeId,
        FieldPharmacogenomicsHaplotypeFromSourceId,
        FieldPharmacogenomicsHaplotypeId,
        FieldPharmacogenomicsIsDirectTarget,
        FieldPharmacogenomicsPgxCategory,
        FieldPharmacogenomicsPhenotypeFromSourceId,
        FieldPharmacogenomicsPhenotypeText,
        FieldPharmacogenomicsTargetFromSourceId,
        FieldPharmacogenomicsVariantFunctionalConsequenceId,
        FieldPharmacogenomicsVariantId,
        FieldPharmacogenomicsVariantRsId,
    ],
)
