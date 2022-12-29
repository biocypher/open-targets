import biocypher
from target_disease_evidence_adapter import (
    TargetDiseaseEvidenceAdapter,
    TargetDiseaseDataset,
    TargetNodeField,
    DiseaseNodeField,
    TargetDiseaseEdgeField,
    GeneOntologyNodeField,
    MousePhenotypeNodeField,
)

datasets = [
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

node_fields = [
    # mandatory fields
    TargetNodeField.TARGET_GENE_ENSG,
    DiseaseNodeField.DISEASE_ACCESSION,
    GeneOntologyNodeField.GENE_ONTOLOGY_ACCESSION,
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_ACCESSION,
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
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_HUMAN_TARGET,
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_MOUSE_TARGET_ENSG,
]

edge_fields = [
    TargetDiseaseEdgeField.INTERACTION_ACCESSION,
    TargetDiseaseEdgeField.TARGET_GENE_ENSG,
    TargetDiseaseEdgeField.DISEASE_ACCESSION,
    TargetDiseaseEdgeField.TYPE,
    TargetDiseaseEdgeField.SCORE,
    TargetDiseaseEdgeField.LITERATURE,
    TargetDiseaseEdgeField.SOURCE,
]


def main():

    driver = biocypher.Driver(
        db_name="full",
        user_schema_config_path="config/target_disease_schema_config.yaml",
    )

    adapter = TargetDiseaseEvidenceAdapter(
        datasets=datasets,
        node_fields=node_fields,
        edge_fields=edge_fields,
    )

    adapter.load_data(
        stats=False,
        show_nodes=False,
        show_edges=False,
    )

    driver.write_nodes(adapter.get_nodes())
    driver.write_edges(adapter.get_edges())

    driver.write_import_call()
    driver.log_duplicates()
    driver.log_missing_bl_types()
    driver.show_ontology_structure()


if __name__ == "__main__":
    main()
