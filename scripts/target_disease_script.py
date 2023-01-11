import biocypher

# VSCode does not add the root directory to the path (by default?). Not sure why
# this works sometimes and not others. This is a workaround.
import sys

sys.path.append("")

from adapters.target_disease_evidence_adapter import (
    TargetDiseaseEvidenceAdapter,
    TargetDiseaseDataset,
    TargetNodeField,
    DiseaseNodeField,
    TargetDiseaseEdgeField,
    GeneOntologyNodeField,
    MousePhenotypeNodeField,
    MouseTargetNodeField,
    MouseModelNodeField,
)

from bccb.uniprot_adapter import (
    Uniprot,
    UniprotNodeType,
    UniprotNodeField,
    UniprotEdgeType,
    UniprotEdgeField,
)

"""
Configuration: select datasets and fields to be imported.

`datasets`: list of datasets to be imported. See 
target_disease_evidence_adapter.py for available datasets or use
`TargetDiseaseDataset` Enum auto-complete.

`node_field`: list of fields to be imported for each of the types of nodes that
the adapter creates. See target_disease_evidence_adapter.py for available fields
or use Enum auto-complete of `TargetNodeField`, `DiseaseNodeField`,
`GeneOntologyNodeField`, `MousePhenotypeNodeField`, `MouseTargetNodeField`. Note
that some fields are mandatory for the functioning of the adapter (primary
identifiers) and some are optional (e.g. gene symbol).

`edge_fields`: list of fields to be imported for each of the relationships that
the adapter creates. See target_disease_evidence_adapter.py for available fields
or use Enum auto-complete of `TargetDiseaseEdgeField`. Note that some fields are
mandatory for the functioning of the adapter (primary identifiers) and some are
optional (e.g.  score).
"""

target_disease_datasets = [
    TargetDiseaseDataset.CANCER_BIOMARKERS,
    TargetDiseaseDataset.CANCER_GENE_CENSUS,
    TargetDiseaseDataset.CHEMBL,
    TargetDiseaseDataset.CLINGEN,
    TargetDiseaseDataset.CRISPR,
    TargetDiseaseDataset.EUROPE_PMC,
    TargetDiseaseDataset.EVA,
    TargetDiseaseDataset.EVA_SOMATIC,
    TargetDiseaseDataset.EXPRESSION_ATLAS,
    TargetDiseaseDataset.GENOMICS_ENGLAND,
    TargetDiseaseDataset.GENE_BURDEN,
    TargetDiseaseDataset.GENE2PHENOTYPE,
    TargetDiseaseDataset.IMPC,
    TargetDiseaseDataset.INTOGEN,
    TargetDiseaseDataset.ORPHANET,
    TargetDiseaseDataset.OT_GENETICS_PORTAL,
    TargetDiseaseDataset.PROGENY,
    TargetDiseaseDataset.REACTOME,
    TargetDiseaseDataset.SLAP_ENRICH,
    TargetDiseaseDataset.SYSBIO,
    TargetDiseaseDataset.UNIPROT_VARIANTS,
    TargetDiseaseDataset.UNIPROT_LITERATURE,
]

target_disease_node_fields = [
    # mandatory fields
    TargetNodeField.TARGET_GENE_ENSG,
    DiseaseNodeField.DISEASE_ACCESSION,
    GeneOntologyNodeField.GENE_ONTOLOGY_ACCESSION,
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_ACCESSION,
    MouseTargetNodeField.MOUSE_TARGET_ENSG,
    # optional target (gene) fields
    TargetNodeField.TARGET_GENE_SYMBOL,
    TargetNodeField.TARGET_GENE_BIOTYPE,
    # optional disease fields
    DiseaseNodeField.DISEASE_CODE,
    DiseaseNodeField.DISEASE_NAME,
    DiseaseNodeField.DISEASE_DESCRIPTION,
    DiseaseNodeField.DISEASE_ONTOLOGY,
    # optional gene ontology fields
    GeneOntologyNodeField.GENE_ONTOLOGY_NAME,
    # optional mouse phenotype fields
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_LABEL,
    # optional mouse target fields
    MouseTargetNodeField.MOUSE_TARGET_SYMBOL,
    MouseTargetNodeField.MOUSE_TARGET_MGI,
    MouseTargetNodeField.HUMAN_TARGET_ENGS,
]

target_disease_edge_fields = [
    # mandatory fields
    TargetDiseaseEdgeField.INTERACTION_ACCESSION,
    TargetDiseaseEdgeField.TARGET_GENE_ENSG,
    TargetDiseaseEdgeField.DISEASE_ACCESSION,
    TargetDiseaseEdgeField.TYPE,
    TargetDiseaseEdgeField.SOURCE,
    # optional fields
    TargetDiseaseEdgeField.SCORE,
    TargetDiseaseEdgeField.LITERATURE,
]

uniprot_node_types = [
    UniprotNodeType.PROTEIN,
]

uniprot_node_fields = [
    UniprotNodeField.PROTEIN_NAMES,
    UniprotNodeField.PROTEIN_LENGTH,
    UniprotNodeField.PROTEIN_MASS,
    UniprotNodeField.PROTEIN_ENSEMBL_GENE_IDS,
]

uniprot_edge_types = [
    UniprotEdgeType.GENE_TO_PROTEIN,
]

uniprot_edge_fields = [
    UniprotEdgeField.GENE_ENSEMBL_GENE_ID,
]


def main():
    """
    Main function running the import using BioCypher and the adapter.
    """

    # Start BioCypher
    driver = biocypher.Driver(
        db_name="full",
        user_schema_config_path="config/target_disease_schema_config.yaml",
    )

    # Load data

    # Open Targets
    target_disease_adapter = TargetDiseaseEvidenceAdapter(
        datasets=target_disease_datasets,
        node_fields=target_disease_node_fields,
        edge_fields=target_disease_edge_fields,
        test_mode=True,
    )

    target_disease_adapter.load_data(
        stats=False,
        show_nodes=False,
        show_edges=False,
    )

    # UniProt
    uniprot_adapter = Uniprot(
        organism="9606",
        node_types=uniprot_node_types,
        node_fields=uniprot_node_fields,
        edge_types=uniprot_edge_types,
        edge_fields=uniprot_edge_fields,
        test_mode=True,
    )

    uniprot_adapter.download_uniprot_data(
        cache=True,
        retries=5,
    )

    # Write nodes
    driver.write_nodes(target_disease_adapter.get_nodes())
    driver.write_nodes(uniprot_adapter.get_nodes())

    # Write edges
    driver.write_edges(uniprot_adapter.get_edges())

    # Write OTAR edges in batches to avoid memory issues
    batches = target_disease_adapter.get_edge_batches()
    for batch in batches:
        driver.write_edges(target_disease_adapter.get_edges(batch_number=batch))

    # Post import functions
    driver.write_import_call()
    driver.log_duplicates()
    driver.log_missing_bl_types()
    driver.show_ontology_structure()


if __name__ == "__main__":
    main()
