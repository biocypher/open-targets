from target_disease_evidence_adapter import TargetDiseaseEvidenceAdapter, TargetDiseaseDataset, TargetDiseaseNodeField
import biocypher

datasets = [
    TargetDiseaseDataset.SYSBIO,
    TargetDiseaseDataset.PROGENY,
]

node_fields = [
    TargetDiseaseNodeField.DISEASE_ACCESSION,
    TargetDiseaseNodeField.TARGET_GENE_ENSG,
]

def main():

    driver = biocypher.Driver(
        user_schema_config_path="config/target_disease_schema_config.yaml",
    )

    adapter = TargetDiseaseEvidenceAdapter(
        datasets=datasets,
        node_fields=node_fields,
        edge_fields="None",
    )

    adapter.load_data()

    driver.write_nodes(adapter.get_nodes())

    driver.write_import_call()
    driver.log_duplicates()
    driver.log_missing_bl_types()
    driver.show_ontology_structure()

if __name__ == "__main__":
    main()

