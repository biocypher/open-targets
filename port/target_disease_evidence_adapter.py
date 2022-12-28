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
    IMPC = "impc"
    INTOGEN = "intogen"
    ORPHANET = "orphanet"
    OT_GENETICS_PORTAL = "ot_genetics_portal"
    PROGENY = "progeny"
    REACTOME = "reactome"
    SLAP_ENRICH = "slapenrich"
    SYSBIO = "sysbio"
    UNIPROT_VARIANTS = "uniprot_variants"
    UNIPROT_LITERATURE = "uniprot_literature"


class TargetDiseaseDatasetLicence(Enum):
    CANCER_BIOMARKERS = "NA"  # TODO
    CANCER_GENE_CENSUS = "Commercial use for Open Targets"
    CHEMBL = "CC BY-SA 3.0"
    CLINGEN = "CC0 1.0"
    CRISPR = "NA"
    EUROPE_PMC = "CC BY-NC 4.0"  # actually can be open access, CC0, CC BY, or CC BY-NC
    EVA = "EMBL-EBI terms of use"
    EVA_SOMATIC = "EMBL-EBI terms of use"
    EXPRESSION_ATLAS = "CC BY 4.0"
    GENOMICS_ENGLAND = "Commercial use for Open Targets"
    GENE_BURDEN = "NA"  # TODO
    GENE2PHENOTYPE = "EMBL-EBI terms of use"
    IMPC = "NA"  # TODO
    INTOGEN = "CC0 1.0"
    ORPHANET = "CC BY 4.0"
    OT_GENETICS_PORTAL = "EMBL-EBI terms of use"
    PROGENY = "Apache 2.0"
    REACTOME = "CC BY 4.0"
    SLAP_ENRICH = "MIT"
    SYSBIO = "NA"  # TODO
    UNIPROT_VARIANTS = "CC BY 4.0"
    UNIPROT_LITERATURE = "CC BY 4.0"


class TargetNodeField(Enum):
    # mandatory fields
    TARGET_GENE_ENSG = "id"

    # optional fields
    TARGET_GENE_SYMBOL = "approvedSymbol"
    TARGET_GENE_BIOTYPE = "biotype"
    TARGET_TRANSCRIPT_IDS = "transcriptIds"
    TARGET_CANONICAL_TRANSCRIPT = "canonicalTranscript"
    TARGET_CANONICAL_EXONS = "canonicalExons"
    TARGET_GENOMIC_LOCATIONS = "genomicLocation"
    TARGET_ALTERNATIVE_GENES = "alternativeGenes"
    TARGET_APPROVED_NAME = "approvedName"
    TARGET_GENE_ONTOLOGY_ANNOTATIONS = "go"
    TARGET_HALLMARKS = "hallmarks"
    TARGET_ALL_SYNONYMS = "synonyms"
    TARGET_GENE_SYMBOL_SYNONYMS = "symbolSynonyms"
    TARGET_NAME_SYNONYMS = "nameSynonyms"
    TARGET_FUNCTIONAL_DESCRIPTIONS = "functionDescriptions"
    TARGET_SUBCELLULAR_LOCATIONS = "subcellularLocations"
    TARGET_CLASS = "targetClass"
    TARGET_OBSOLETE_GENE_SYMBOLS = "obsoleteSymbols"
    TARGET_OBSOLETE_GENE_NAMES = "obsoleteNames"
    TARGET_CONSTRAINT = "constraint"
    TARGET_TEP = "tep"
    TARGET_PROTEIN_IDS = "proteinIds"
    TARGET_DATABASE_XREFS = "dbXrefs"
    TARGET_CHEMICAL_PROBES = "chemicalProbes"
    TARGET_HOMOLOGUES = "homologues"
    TARGET_TRACTABILITY = "tractability"
    TARGET_SAFETY_LIABILITIES = "safetyLiabilities"
    TARGET_PATHWAYS = "pathways"


class DiseaseNodeField(Enum):
    # mandatory fields
    DISEASE_ACCESSION = "id"

    # optional fields
    DISEASE_CODE = "code"
    DISEASE_DATABASE_XREFS = "dbXRefs"
    DISEASE_DESCRIPTION = "description"
    DISEASE_NAME = "name"
    DISEASE_DIRECT_LOCATION_IDS = "directLocationIds"
    DISEASE_OBSOLETE_TERMS = "obsoleteTerms"
    DISEASE_PARENTS = "parents"
    DISEASE_SKO = "sko"
    DISEASE_SYNONYMS = "synonyms"
    DISEASE_ANCESTORS = "ancestors"
    DISEASE_DESCENDANTS = "descendants"
    DISEASE_CHILDREN = "children"
    DISEASE_THERAPEUTIC_AREAS = "therapeuticAreas"
    DISEASE_INDIRECT_LOCATION_IDS = "indirectLocationIds"
    DISEASE_ONTOLOGY = "ontology"


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
        edge_fields: list = None,
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

        if not TargetNodeField.TARGET_GENE_ENSG in self.node_fields:
            raise ValueError("TargetNodeField.TARGET_GENE_ENSG must be provided")

        if not DiseaseNodeField.DISEASE_ACCESSION in self.node_fields:
            raise ValueError("DiseaseNodeField.DISEASE_ACCESSION must be provided")

        # Create SparkSession
        self.spark = SparkSession.builder.master("local").appName("port").getOrCreate()

    def load_data(
        self, stats: bool = False, show_nodes: bool = False, show_edges: bool = False
    ):

        # Read in evidence data and target / disease annotations
        evidence_path = "data/ot_files/evidence"
        self.evidence_df = self.spark.read.parquet(evidence_path)

        target_path = "data/ot_files/targets"
        self.target_df = self.spark.read.parquet(target_path)

        disease_path = "data/ot_files/diseases"
        self.disease_df = self.spark.read.parquet(disease_path)

        if stats:

            # print schema
            print(self.evidence_df.printSchema())
            print(self.target_df.printSchema())
            print(self.disease_df.printSchema())

            # print number of rows
            print(f"Length of evidence data: {self.evidence_df.count()} entries")
            print(f"Length of target data: {self.target_df.count()} entries")
            print(f"Length of disease data: {self.disease_df.count()} entries")

            # print number of rows per datasource
            self.evidence_df.groupBy("datasourceId").count().show(100)

        if show_edges:
            for dataset in [field.value for field in self.datasets]:
                self.evidence_df.where(self.evidence_df.datasourceId == dataset).show(
                    1, 50, True
                )

        if show_nodes:
            self.target_df.show(1, 50, True)
            self.disease_df.show(1, 50, True)

    def show_datasources(self):

        # collect all distinct datasourceId values
        datasources = self.evidence_df.select("datasourceId").distinct().collect()

        # convert to list
        self.datasources = [x.datasourceId for x in datasources]
        print(self.datasources)

    def get_nodes(self):

        # Targets
        # Select columns of interest
        target_df = self.target_df.select(
            [
                field.value
                for field in self.node_fields
                if isinstance(field, TargetNodeField)
            ]
        )

        # yield target nodes
        for target in target_df.collect():

            # normalize id
            _id = normalize_curie(f"ensembl:{target.id}")

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = "Open Targets"
            _props["licence"] = "https://platform-docs.opentargets.org/licence"

            for field in self.node_fields:

                if not isinstance(field, TargetNodeField):
                    continue

                if target[field.value]:
                    _props[field.value] = target[field.value]

            yield (_id, "gene", _props)

        # Diseases
        # Select columns of interest
        disease_df = self.disease_df.select(
            [
                field.value
                for field in self.node_fields
                if isinstance(field, DiseaseNodeField)
            ]
        )

        for disease in disease_df.collect():

            _id, _type = self._process_disease_id_and_type(disease.id)

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = "open targets"
            _props["licence"] = "https://platform-docs.opentargets.org/licence"

            for field in self.node_fields:

                if not isinstance(field, DiseaseNodeField):
                    continue

                if disease[field.value]:
                    _props[field.value] = disease[field.value]

            yield (_id, _type, _props)

    def get_edges(self):

        # select columns of interest
        edge_df = self.evidence_df.where(
            self.evidence_df.datasourceId.isin([field.value for field in self.datasets])
        ).select([field.value for field in self.edge_fields])

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

            disease_id, _type = self._process_disease_id_and_type(row.diseaseId)

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
