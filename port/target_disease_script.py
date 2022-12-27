from target_disease_evidence_adapter import TargetDiseaseEvidenceAdapter, TargetDiseaseDataset, TargetDiseaseNodeField, TargetDiseaseEdgeField
import biocypher

datasets = [
    TargetDiseaseDataset.CLINGEN,
    TargetDiseaseDataset.EVA_SOMATIC,
    TargetDiseaseDataset.GENE2PHENOTYPE,
    TargetDiseaseDataset.INTOGEN,
    TargetDiseaseDataset.PROGENY,
    TargetDiseaseDataset.SYSBIO,
    TargetDiseaseDataset.UNIPROT_LITERATURE,
]

node_fields = [
    TargetDiseaseNodeField.DISEASE_ACCESSION,
    TargetDiseaseNodeField.TARGET_GENE_ENSG,
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
        db_name="small",
        user_schema_config_path="config/target_disease_schema_config.yaml",
    )

    adapter = TargetDiseaseEvidenceAdapter(
        datasets=datasets,
        node_fields=node_fields,
        edge_fields=edge_fields,
    )

    adapter.load_data(
        stats=False,
        show=False,
    )

    driver.write_nodes(adapter.get_nodes())
    driver.write_edges(adapter.get_edges())

    driver.write_import_call()
    driver.log_duplicates()
    driver.log_missing_bl_types()
    driver.show_ontology_structure()

if __name__ == "__main__":
    main()

