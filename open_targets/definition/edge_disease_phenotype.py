"""Acquisition definition that acquires edges between diseases and phenotypes."""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionEdgeAcquisitionDefinition
from open_targets.adapter.output import EdgeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation
from open_targets.data.schema import (
    DatasetDiseaseToPhenotype,
    FieldDiseaseToPhenotypeDisease,
    FieldDiseaseToPhenotypeEvidence,
    FieldDiseaseToPhenotypeEvidenceElementAspect,
    FieldDiseaseToPhenotypeEvidenceElementBioCuration,
    FieldDiseaseToPhenotypeEvidenceElementDiseaseFromSource,
    FieldDiseaseToPhenotypeEvidenceElementDiseaseFromSourceId,
    FieldDiseaseToPhenotypeEvidenceElementDiseaseName,
    FieldDiseaseToPhenotypeEvidenceElementEvidenceType,
    FieldDiseaseToPhenotypeEvidenceElementFrequency,
    FieldDiseaseToPhenotypeEvidenceElementModifiers,
    FieldDiseaseToPhenotypeEvidenceElementOnset,
    FieldDiseaseToPhenotypeEvidenceElementQualifier,
    FieldDiseaseToPhenotypeEvidenceElementQualifierNot,
    FieldDiseaseToPhenotypeEvidenceElementReferences,
    FieldDiseaseToPhenotypeEvidenceElementResource,
    FieldDiseaseToPhenotypeEvidenceElementSex,
    FieldDiseaseToPhenotypePhenotype,
)
from open_targets.definition.helper import get_arrow_expression

edge_disease_phenotype: Final[AcquisitionDefinition[EdgeInfo]] = ExpressionEdgeAcquisitionDefinition(
    scan_operation=ExplodingScanOperation(
        dataset=DatasetDiseaseToPhenotype,
        exploded_field=FieldDiseaseToPhenotypeEvidence,
    ),
    primary_id=get_arrow_expression(FieldDiseaseToPhenotypeDisease, FieldDiseaseToPhenotypePhenotype),
    source=FieldDiseaseToPhenotypeDisease,
    target=FieldDiseaseToPhenotypePhenotype,
    label="DISEASE_TO_PHENOTYPE_ASSOCIATION",
    properties=[
        FieldDiseaseToPhenotypeEvidenceElementAspect,
        FieldDiseaseToPhenotypeEvidenceElementBioCuration,
        FieldDiseaseToPhenotypeEvidenceElementDiseaseFromSource,
        FieldDiseaseToPhenotypeEvidenceElementDiseaseFromSourceId,
        FieldDiseaseToPhenotypeEvidenceElementDiseaseName,
        FieldDiseaseToPhenotypeEvidenceElementEvidenceType,
        FieldDiseaseToPhenotypeEvidenceElementFrequency,
        FieldDiseaseToPhenotypeEvidenceElementModifiers,
        FieldDiseaseToPhenotypeEvidenceElementOnset,
        FieldDiseaseToPhenotypeEvidenceElementQualifier,
        FieldDiseaseToPhenotypeEvidenceElementQualifierNot,
        FieldDiseaseToPhenotypeEvidenceElementReferences,
        FieldDiseaseToPhenotypeEvidenceElementResource,
        FieldDiseaseToPhenotypeEvidenceElementSex,
    ],
)
