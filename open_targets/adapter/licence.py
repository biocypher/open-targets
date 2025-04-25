"""Licence enum and utility functions."""

from enum import Enum


class License(str, Enum):
    """Enumeration of licenses used in Open Targets datasets."""

    APACHE_2_0 = "Apache 2.0"
    CC0_1_0 = "CC0 1.0"
    CC_BY_4_0 = "CC BY 4.0"
    CC_BY_SA_3_0 = "CC BY-SA 3.0"
    CC_BY_NC_4_0 = "CC BY-NC 4.0"
    EMBL_EBI = "EMBL-EBI terms of use"
    MIT = "MIT"
    COMMERCIAL_OT = "Commercial use for Open Targets"
    NOT_AVAILABLE = "NA"
    UNKNOWN = "Unknown"


def get_datasource_license(dataset_id: str) -> str:
    """Get the license for a given dataset ID."""
    licence = None
    match dataset_id:
        case "progeny":
            licence = License.APACHE_2_0
        case "intogen" | "clingen":
            licence = License.CC0_1_0
        case "expression_atlas" | "orphanet" | "reactome" | "uniprot_variants" | "uniprot_literature":
            licence = License.CC_BY_4_0
        case "chembl":
            licence = License.CC_BY_SA_3_0
        case "europepmc":
            licence = License.CC_BY_NC_4_0
        case "eva" | "eva_somatic" | "gene2phenotype" | "ot_genetics_portal":
            licence = License.EMBL_EBI
        case "slapenrich":
            licence = License.MIT
        case "cancer_gene_census" | "genomics_england":
            licence = License.COMMERCIAL_OT
        case "cancer_biomarkers" | "crispr" | "gene_burden" | "impc" | "sysbio":
            licence = License.NOT_AVAILABLE
        case _:
            licence = License.UNKNOWN
    return str(licence)
