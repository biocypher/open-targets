"""Acquisition definition that acquires nodes of pharmacogenomics evidence."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
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
    FieldPharmacogenomicsStudyId,
    FieldPharmacogenomicsTargetFromSourceId,
    FieldPharmacogenomicsVariantFunctionalConsequenceId,
    FieldPharmacogenomicsVariantRsId,
)

node_pharmacogenomics_evidence: Final[AcquisitionDefinition[NodeInfo]] = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetPharmacogenomics),
    primary_id=FieldPharmacogenomicsStudyId,
    label="PHARMACOGENOMICS_EVIDENCE",
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
        FieldPharmacogenomicsVariantRsId,
    ],
)
