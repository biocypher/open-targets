from typing import Optional
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, DataFrame, functions as F
from enum import Enum
from bioregistry import normalize_curie
from biocypher._logger import logger
from tqdm import tqdm
import functools


class TargetDiseaseDataset(Enum):
    """
    Enum of all the datasets used in the target-disease evidence pipeline.
    Values are the spellings used in the Open Targets parquet files.
    """

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


_licences = {
    "cancer_biomarkers": "NA",  # TODO
    "cancer_gene_census": "Commercial use for Open Targets",
    "chembl": "CC BY-SA 3.0",
    "clingen": "CC0 1.0",
    "crispr": "NA",  # TODO
    "europepmc": "CC BY-NC 4.0",  # can be open access, CC0, CC BY, or CC BY-NC
    "eva": "EMBL-EBI terms of use",
    "eva_somatic": "EMBL-EBI terms of use",
    "expression_atlas": "CC BY 4.0",
    "genomics_england": "Commercial use for Open Targets",
    "gene_burden": "NA",  # TODO
    "gene2phenotype": "EMBL-EBI terms of use",
    "impc": "NA",  # TODO
    "intogen": "CC0 1.0",
    "orphanet": "CC BY 4.0",
    "ot_genetics_portal": "EMBL-EBI terms of use",
    "progeny": "Apache 2.0",
    "reactome": "CC BY 4.0",
    "slapenrich": "MIT",
    "sysbio": "NA",  # TODO
    "uniprot_variants": "CC BY 4.0",
    "uniprot_literature": "CC BY 4.0",
}


class TargetNodeField(Enum):
    """
    Enum of all the fields in the target dataset. Values are the spellings used
    in the Open Targets parquet files.
    """

    _PRIMARY_ID = "id"

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
    """
    Enum of all the fields in the disease dataset. Values are the spellings used
    in the Open Targets parquet files.
    """

    _PRIMARY_ID = "id"

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


class GeneOntologyNodeField(Enum):
    """
    Enum of all the fields in the gene ontology dataset. Values are the
    spellings used in the Open Targets parquet files.
    """

    _PRIMARY_ID = "id"

    # mandatory fields
    GENE_ONTOLOGY_ACCESSION = "id"
    # optional fields
    GENE_ONTOLOGY_NAME = "name"


class MousePhenotypeNodeField(Enum):
    """
    Enum of all the fields in the mouse phenotype dataset. Values are the
    spellings used in the Open Targets parquet files.
    """

    _PRIMARY_ID = "modelPhenotypeId"

    # mandatory fields
    MOUSE_PHENOTYPE_ACCESSION = "modelPhenotypeId"

    # optional fields
    MOUSE_PHENOTYPE_LABEL = "modelPhenotypeLabel"


class MouseTargetNodeField(Enum):
    """
    Enum of all the fields in the mouse phenotype dataset related to murine
    targets of each biological model. Values are the spellings used in the Open
    Targets parquet files.
    """

    _PRIMARY_ID = "targetInModelEnsemblId"

    # mandatory fields
    MOUSE_TARGET_ENSG = "targetInModelEnsemblId"

    # alternative ids
    MOUSE_TARGET_SYMBOL = "targetInModel"
    MOUSE_TARGET_MGI = "targetInModelMgiId"

    # human target ensembl id
    HUMAN_TARGET_ENGS = "targetFromSourceId"


class MouseModelNodeField(Enum):
    """
    Enum of all the fields in the mouse phenotype dataset related to the mouse
    model. Values are the spellings used in the Open Targets parquet files.
    """

    _PRIMARY_ID = "biologicalModels"

    MOUSE_PHENOTYPE_MODELS = "biologicalModels"
    MOUSE_PHENOTYPE_CLASSES = "modelPhenotypeClasses"


class TargetDiseaseEdgeField(Enum):
    """
    Enum of all the fields in the target-disease dataset. Used to generate the
    bulk of relationships in the graph. Values are the spellings used in the
    Open Targets parquet files.
    """

    INTERACTION_ACCESSION = "id"
    TARGET_GENE_ENSG = "targetId"
    DISEASE_ACCESSION = "diseaseId"
    TYPE = "datatypeId"
    SOURCE = "datasourceId"
    LITERATURE = "literature"
    SCORE = "score"


class TargetDiseaseEvidenceAdapter:
    def __init__(
        self,
        datasets: list[Enum] = None,
        node_fields: list[Enum] = None,
        edge_fields: list = None,
        test_mode: bool = False,
    ):
        self.datasets = datasets
        self.node_fields = node_fields
        self.edge_fields = edge_fields
        self.test_mode = test_mode

        if not self.datasets:
            raise ValueError("datasets must be provided")

        if not self.node_fields:
            raise ValueError("node_fields must be provided")

        if not self.edge_fields:
            raise ValueError("edge_fields must be provided")

        if not TargetNodeField.TARGET_GENE_ENSG in self.node_fields:
            raise ValueError(
                "TargetNodeField.TARGET_GENE_ENSG must be provided"
            )

        if not DiseaseNodeField.DISEASE_ACCESSION in self.node_fields:
            raise ValueError(
                "DiseaseNodeField.DISEASE_ACCESSION must be provided"
            )

        if self.test_mode:
            logger.warning(
                "Open Targets adapter: Test mode is enabled. "
                "Only processing 100 rows."
            )

        logger.info("Creating Spark session.")

        # Set up Spark context
        conf = (
            SparkConf()
            .setAppName("otar_biocypher")
            .setMaster("local")
            .set("spark.driver.memory", "4g")
            .set("spark.executor.memory", "4g")
        )
        self.sc = SparkContext(conf=conf)

        # Create SparkSession
        self.spark = (
            SparkSession.builder.master("local")
            .appName("otar_biocypher")
            .getOrCreate()
        )

    def load_data(
        self,
        stats: bool = False,
        show_nodes: bool = False,
        show_edges: bool = False,
    ):

        logger.info("Loading data from disk.")

        # Read in evidence data and target / disease annotations
        evidence_path = "data/ot_files/evidence"
        self.evidence_df = self.spark.read.parquet(evidence_path)

        target_path = "data/ot_files/targets"
        self.target_df = self.spark.read.parquet(target_path)

        disease_path = "data/ot_files/diseases"
        self.disease_df = self.spark.read.parquet(disease_path)

        go_path = "data/ot_files/go"
        self.go_df = self.spark.read.parquet(go_path)

        mp_path = "data/ot_files/mousePhenotypes"
        self.mp_df = self.spark.read.parquet(mp_path)

        if stats:

            # print schema
            print(self.evidence_df.printSchema())
            print(self.target_df.printSchema())
            print(self.disease_df.printSchema())
            print(self.go_df.printSchema())
            print(self.mp_df.printSchema())

            # print number of rows
            print(
                f"Length of evidence data: {self.evidence_df.count()} entries"
            )
            print(f"Length of target data: {self.target_df.count()} entries")
            print(f"Length of disease data: {self.disease_df.count()} entries")
            print(f"Length of GO data: {self.go_df.count()} entries")
            print(
                f"Length of Mouse Phenotype data: {self.mp_df.count()} entries"
            )

            # print number of rows per datasource
            self.evidence_df.groupBy("datasourceId").count().show(100)

        if show_edges:
            for dataset in [field.value for field in self.datasets]:
                self.evidence_df.where(
                    self.evidence_df.datasourceId == dataset
                ).show(1, 50, True)

        if show_nodes:
            self.target_df.show(1, 50, True)
            self.disease_df.show(1, 50, True)
            self.go_df.show(1, 50, True)
            self.mp_df.show(1, 50, True)

    def show_datasources(self):
        """
        Utility function to get all datasources in the evidence data.
        """

        # collect all distinct datasourceId values
        datasources = (
            self.evidence_df.select("datasourceId").distinct().collect()
        )

        # convert to list
        self.datasources = [x.datasourceId for x in datasources]
        print(self.datasources)

    def _yield_node_type(
        self,
        df: DataFrame,
        node_field_type: Enum,
        biolink_type: Optional[str] = None,
    ):
        """
        Yield the node type from the dataframe.
        """

        # Select columns of interest
        df = df.select(
            [
                field.value
                for field in self.node_fields
                if isinstance(field, node_field_type)
            ]
        )

        logger.info(f"Generating nodes of {node_field_type}.")

        if self.test_mode:
            df = df.limit(100)

        for row in tqdm(df.collect()):

            # normalize id
            _id, _type = _process_id_and_type(
                row[node_field_type._PRIMARY_ID.value], biolink_type
            )

            # switch mouse gene type
            if node_field_type == MouseTargetNodeField:
                _type = "mouse gene"

            if not _id:
                continue

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = "Open Targets"
            _props["licence"] = "https://platform-docs.opentargets.org/licence"

            for field in self.node_fields:

                if not isinstance(field, node_field_type):
                    continue

                if row[field.value]:
                    _props[field.value] = row[field.value]

            yield (_id, _type, _props)

    def get_nodes(self):
        """
        Yield nodes from the target and disease dataframes.
        """

        # Targets
        yield from self._yield_node_type(
            self.target_df, TargetNodeField, "ensembl"
        )

        # Diseases
        yield from self._yield_node_type(self.disease_df, DiseaseNodeField)

        # Gene Ontology
        yield from self._yield_node_type(self.go_df, GeneOntologyNodeField)

        # Mouse Phenotypes
        only_mp_df = self.mp_df.select(
            [field.value for field in MousePhenotypeNodeField]
        ).dropDuplicates()
        yield from self._yield_node_type(only_mp_df, MousePhenotypeNodeField)

        # Mouse Targets
        mouse_target_df = self.mp_df.select(
            [field.value for field in MouseTargetNodeField]
        ).dropDuplicates()
        yield from self._yield_node_type(
            mouse_target_df, MouseTargetNodeField, "ensembl"
        )

    def get_edge_batches(self):
        """
        Create a column with partition number in the evidence dataframe and
        return a list of batch numbers.
        """

        logger.info("Generating batches.")

        # select columns of interest
        self.evidence_df = self.evidence_df.where(
            self.evidence_df.datasourceId.isin(
                [field.value for field in self.datasets]
            )
        ).select([field.value for field in self.edge_fields])

        # add partition number to self.evidence_df as column
        self.evidence_df = self.evidence_df.withColumn(
            "partition_num", F.spark_partition_id()
        )
        self.evidence_df.persist()

        self.batches = [
            int(row.partition_num)
            for row in self.evidence_df.select("partition_num")
            .distinct()
            .collect()
        ]

        logger.info(f"Generated {len(self.batches)} batches.")

        return self.batches

    def get_edges(self, batch_number: int):
        """
        Yield edges from the evidence dataframe per batch.
        """

        # Check if self.evidence_df has column partition_num
        if "partition_num" not in self.evidence_df.columns:
            raise ValueError(
                "self.evidence_df does not have column partition_num. "
                "Please run get_edge_batches() first."
            )

        logger.info("Generating edges.")

        logger.info(
            f"Processing batch {batch_number+1} of {len(self.batches)}."
        )

        yield from self._process_edges(
            self.evidence_df.where(
                self.evidence_df.partition_num == batch_number
            )
        )

    def _process_edges(self, batch):
        """
        Process one batch of edges.
        """

        logger.info(f"Batch size: {batch.count()} edges.")

        if self.test_mode:
            # limit batch df to 100 rows
            batch = batch.limit(100)

        # yield edges per row of edge_df, skipping null values
        for row in tqdm(batch.collect()):

            # collect properties from fields, skipping null values
            properties = {}
            for field in self.edge_fields:
                # skip disease and target ids, relationship id, and datatype id
                # as they are encoded in the relationship
                if field not in [
                    TargetDiseaseEdgeField.LITERATURE,
                    TargetDiseaseEdgeField.SCORE,
                    TargetDiseaseEdgeField.SOURCE,
                ]:
                    continue

                if field == TargetDiseaseEdgeField.SOURCE:
                    properties["source"] = row[field.value]
                    properties["licence"] = _find_licence(row[field.value])
                elif row[field.value]:
                    properties[field.value] = row[field.value]

            properties["version"] = "22.11"

            disease_id, _ = _process_id_and_type(row.diseaseId)
            gene_id, _ = _process_id_and_type(row.targetId, "ensembl")

            yield (
                row.id,
                gene_id,
                disease_id,
                row.datatypeId,
                properties,
            )


@functools.lru_cache()
def _process_id_and_type(inputId: str, _type: Optional[str] = None):
    """
    Process diseaseId and diseaseType fields from evidence data. Process
    gene (ENSG) ids.
    """

    if not inputId:
        return (None, None)

    if _type:

        _id = normalize_curie(f"{_type}:{inputId}")

        return (_id, _type)

    # detect delimiter (either _ or :)
    if "_" in inputId:

        _type = inputId.split("_")[0].lower()

        # special case for OTAR TODO
        if _type == "otar":
            _id = f"otar:{inputId.split('_')[1]}"
        else:
            _id = normalize_curie(inputId, sep="_")

    elif ":" in inputId:

        _type = inputId.split(":")[0].lower()
        _id = normalize_curie(inputId, sep=":")

    return (_id, _type)


def _find_licence(source: str) -> str:
    """
    Find and return the licence for a source.
    """

    return _licences.get(source, "Unknown")
