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

class TargetDiseaseEdgeField(Enum):
    DISEASE_ACCESSION = "diseaseId"
    INTERACTION_ACCESSION = "id"
    LITERATURE = "literature"
    TARGET_GENE_ENSG = "targetId"
    SCORE = "score"
    SOURCE = "datasourceId"
    TYPE = "datatypeId"

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

    def load_data(self, stats: bool = False, show: bool = False):

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

        if show:
            for dataset in [field.value for field in self.datasets]:
                self.full_df.where(self.full_df.datasourceId == dataset) \
                    .show(1, 50, True)

    def show_datasources(self):

        # collect all distinct datasourceId values
        datasources = self.full_df.select("datasourceId").distinct().collect()

        # convert to list
        self.datasources = [x.datasourceId for x in datasources]
        print(self.datasources)

    def get_nodes(self):

        # Select columns of interest
        node_df = self.full_df.where(self.full_df.datasourceId.isin(
            [field.value for field in self.datasets]
        )).select(
            [field.value for field in self.node_fields]
        )  
            
        # get distinct values for each column
        target_ids = node_df.select("targetId").distinct().collect()
        disease_ids = node_df.select("diseaseId").distinct().collect()


        # yield target and disease ids
        for target_id in target_ids:
            
            # normalize id
            _id = normalize_curie(f"ensembl:{target_id.targetId}")

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = ["open targets"]
            _props["licence"] = ["https://platform-docs.opentargets.org/licence"] 
            # TODO single licences

            yield (_id, "gene", _props)

        for disease_id in disease_ids:

            _id, _type = self._process_disease_id_and_type(disease_id.diseaseId)

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = ["open targets"]
            _props["licence"] = ["https://platform-docs.opentargets.org/licence"] 
            # TODO single licences

            yield (_id, _type, _props)

    def get_edges(self):
        
        # select columns of interest
        edge_df = self.full_df.where(self.full_df.datasourceId.isin(
            [field.value for field in self.datasets]
        )).select(
            [field.value for field in self.edge_fields]
        )

        # yield edges per row of edge_df, skipping null values
        for row in edge_df.collect():

            # collect properties from fields, skipping null values
            properties = {}
            for field in self.edge_fields:
                if field == TargetDiseaseEdgeField.SOURCE:
                    properties["source"] = row[field.value]
                elif row[field.value]:
                    properties[field.value] = row[field.value]

            properties["version"] = "22.11"
            properties["licence"] = ["https://platform-docs.opentargets.org/licence"]
            # TODO single licences

            disease_id, _ = self._process_disease_id_and_type(row.diseaseId)

            yield (
                row.id, 
                normalize_curie(f"ensembl:{row.targetId}"), 
                disease_id, 
                row.datatypeId, 
                properties,
            )
    
    def _process_disease_id_and_type(self, diseaseId: str):
        """
        Process diseaseId and diseaseType fields from evidence data
        """
        # split id into prefix and accession at _
        _id = diseaseId.split("_")[1]
        _type = diseaseId.split("_")[0].lower()

        # normalize id
        _id = normalize_curie(_type + ":" + _id)

        return (_id, _type)
