import os
from pyspark.sql import SparkSession
from enum import Enum
from bioregistry import normalize_curie

class TargetDiseaseDataset(Enum):
    CANCER_BIOMARKERS = "cancer_biomarkers"
    CANCER_GENE_CENSUS = "cancer_gene_census"
    CHEMBL = "chembl"
    CLINGEN = "clingen"
    CRISPR = "crispr"
    EUROPE_PMC = "europepmc"
    EVA = "eva"
    EVA_SOMATIC = "eva_somatic"
    EXPRESSION_ATLAS = "expression_atlas"
    GENOMICS_ENGLAND = "genomics_england"
    GENE_BURDEN = "gene_burden"
    GENE2PHENOTYPE = "gene2phenotype"
    IMPACT = "impc"
    INTOGEN = "intogen"
    ORPHANET = "orphanet"
    OT_GENETICS_PORTAL = "ot_genetics_portal"
    PROGENY = "progeny"
    REACTOME = "reactome"
    SLAP_ENRICH = "slapenrich"
    SYSBIO = "sysbio"
    UNIPROT_VARIANTS = "uniprot_variants"
    UNIPROT_LITERATURE = "uniprot_literature"

class TargetDiseaseNodeField(Enum):
    DISEASE_ACCESSION = "diseaseId"
    TARGET_GENE_ENSG = "targetId"

class TargetDiseaseEvidenceAdapter:
    def __init__(
        self, 
        datasets: list[Enum] = None,
        node_fields: list[Enum] = None, 
        edge_fields: list = None
    ):
        self.datasets = datasets
        self.node_fields = node_fields
        self.edge_fields = edge_fields

        if not self.datasets:
            raise ValueError("datasets must be provided")

        if not self.node_fields:
            raise ValueError("node_fields must be provided")

        if not self.edge_fields:
            raise ValueError("edge_fields must be provided")
        
        # Create SparkSession
        self.spark = SparkSession.builder \
            .master("local") \
            .appName("port") \
            .getOrCreate()

    def load_data(self, stats: bool = False):

        # Read in evidence data
        self.path = "data/ot_files/evidence"
        self.full_df = self.spark.read.parquet(self.path)

        if stats:

            # print schema
            print(self.full_df.printSchema())

            # print number of rows
            print(f"Length of evidence data: {self.full_df.count()} entries")

            # print number of rows per datasource
            self.full_df.groupBy("datasourceId").count().show(100)

    def show_datasources(self):

        # collect all distinct datasourceId values
        datasources = self.full_df.select("datasourceId").distinct().collect()

        # convert to list
        self.datasources = [x.datasourceId for x in datasources]
        print(self.datasources)

    def get_nodes(self):

        # Select columns of interest
        self.node_df = self.full_df.select("datasourceId", "targetId", "diseaseId")
        
        for datasource in [field.value for field in self.datasets]:
            
            df = self.spark.read.parquet(self.path).where(f"datasourceId = '{datasource}'")
            df.select("targetId", "diseaseId")

            # get distinct values for each column
            target_ids = df.select("targetId").distinct().collect()
            disease_ids = df.select("diseaseId").distinct().collect()

            # yield target and disease ids
            for target_id in target_ids:

                # normalize id
                _id = normalize_curie(f"ensembl:{target_id.targetId}")

                yield (_id, "gene", {})

            for disease_id in disease_ids:

                # split id into prefix and accession at _
                _id = disease_id.diseaseId.split("_")[1]
                _type = disease_id.diseaseId.split("_")[0].lower()

                # normalize id
                _id = normalize_curie(_type + ":" + _id)

                yield (_id, _type, {})
