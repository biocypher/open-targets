"""Summary: rare-variant burden tests linking genes to disease/traits.

Definition for TARGET_DISEASE_ASSOCIATION_GENE_BURDEN nodes: filters Evidence
parquet to gene_burden source to emit rare-variant burden associations. Burden
tests collapse many rare variants in a gene into a single burden score and test
carriers vs non-carriers for disease/trait difference. Arrow logic: sequence rare
variants -> collapse into burden score -> regress burden against phenotype ->
significant beta/OR/p-value -> link gene to disease. Records store regression
effects, p-values, ancestry/cohort info, allelic requirements, and study metadata.
The KG captures these gene-wide rare-variant signals rather than single-variant
hits.
"""

from typing import Final

from open_targets.adapter.acquisition_definition import AcquisitionDefinition, ExpressionNodeAcquisitionDefinition
from open_targets.adapter.expression import FieldExpression, TransformExpression
from open_targets.adapter.output import NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation
from open_targets.data.schema import (
    DatasetEvidenceGeneBurden,
    FieldEvidenceGeneBurdenAllelicRequirements,
    FieldEvidenceGeneBurdenAncestry,
    FieldEvidenceGeneBurdenAncestryId,
    FieldEvidenceGeneBurdenBeta,
    FieldEvidenceGeneBurdenBetaConfidenceIntervalLower,
    FieldEvidenceGeneBurdenBetaConfidenceIntervalUpper,
    FieldEvidenceGeneBurdenDiseaseFromSource,
    FieldEvidenceGeneBurdenDiseaseFromSourceId,
    FieldEvidenceGeneBurdenDiseaseFromSourceMappedId,
    FieldEvidenceGeneBurdenId,
    FieldEvidenceGeneBurdenLiterature,
    FieldEvidenceGeneBurdenOddsRatio,
    FieldEvidenceGeneBurdenOddsRatioConfidenceIntervalLower,
    FieldEvidenceGeneBurdenOddsRatioConfidenceIntervalUpper,
    FieldEvidenceGeneBurdenProjectId,
    FieldEvidenceGeneBurdenPValueExponent,
    FieldEvidenceGeneBurdenPValueMantissa,
    FieldEvidenceGeneBurdenResourceScore,
    FieldEvidenceGeneBurdenScore,
    FieldEvidenceGeneBurdenStatisticalMethod,
    FieldEvidenceGeneBurdenStatisticalMethodOverview,
    FieldEvidenceGeneBurdenStudyCases,
    FieldEvidenceGeneBurdenStudyCasesWithQualifyingVariants,
    FieldEvidenceGeneBurdenStudySampleSize,
    FieldEvidenceGeneBurdenTargetFromSourceId,
    FieldEvidenceGeneBurdenUrls,
    FieldEvidenceGeneBurdenUrlsElementUrl,
)

node_target_disease_association_gene_burden: Final[AcquisitionDefinition[NodeInfo]] = (
    ExpressionNodeAcquisitionDefinition(
        scan_operation=RowScanOperation(dataset=DatasetEvidenceGeneBurden),
        primary_id=FieldEvidenceGeneBurdenId,
        label="TARGET_DISEASE_ASSOCIATION_GENE_BURDEN",
        properties=[
            FieldEvidenceGeneBurdenAllelicRequirements,
            FieldEvidenceGeneBurdenAncestry,
            FieldEvidenceGeneBurdenAncestryId,
            FieldEvidenceGeneBurdenBeta,
            FieldEvidenceGeneBurdenBetaConfidenceIntervalLower,
            FieldEvidenceGeneBurdenBetaConfidenceIntervalUpper,
            FieldEvidenceGeneBurdenDiseaseFromSource,
            FieldEvidenceGeneBurdenDiseaseFromSourceId,
            FieldEvidenceGeneBurdenDiseaseFromSourceMappedId,
            FieldEvidenceGeneBurdenLiterature,
            FieldEvidenceGeneBurdenOddsRatio,
            FieldEvidenceGeneBurdenOddsRatioConfidenceIntervalLower,
            FieldEvidenceGeneBurdenOddsRatioConfidenceIntervalUpper,
            FieldEvidenceGeneBurdenPValueExponent,
            FieldEvidenceGeneBurdenPValueMantissa,
            FieldEvidenceGeneBurdenProjectId,
            FieldEvidenceGeneBurdenResourceScore,
            FieldEvidenceGeneBurdenScore,
            FieldEvidenceGeneBurdenStatisticalMethod,
            FieldEvidenceGeneBurdenStatisticalMethodOverview,
            FieldEvidenceGeneBurdenStudyCases,
            FieldEvidenceGeneBurdenStudyCasesWithQualifyingVariants,
            FieldEvidenceGeneBurdenStudySampleSize,
            FieldEvidenceGeneBurdenTargetFromSourceId,
            (
                FieldEvidenceGeneBurdenUrls.name,
                TransformExpression(
                    FieldExpression(FieldEvidenceGeneBurdenUrls),
                    lambda urls: (
                        None
                        if not urls
                        else [
                            str(url[FieldEvidenceGeneBurdenUrlsElementUrl])
                            for url in urls
                            if url is not None and url[FieldEvidenceGeneBurdenUrlsElementUrl] is not None
                        ]
                    ),
                ),
            ),
        ],
    )
)
