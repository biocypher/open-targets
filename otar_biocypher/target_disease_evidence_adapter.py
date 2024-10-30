from typing import Optional, Type
from enum import Enum
from bioregistry.resolve import normalize_curie
from biocypher._logger import logger
from tqdm import tqdm
from pyarrow.parquet import ParquetFile
import functools
import base64
import duckdb


class TargetDiseaseDataset(Enum):
    """
    Enum of all the datasets used in the target-disease evidence pipeline.
    Values are the spellings used in the Open Targets parquet files.
    """

    # TODO: Where does this info come from?
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

    # mandatory fields
    TARGET_GENE_ENSG = "id"
    _PRIMARY_ID = TARGET_GENE_ENSG

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

    # mandatory fields
    DISEASE_ACCESSION = "id"
    _PRIMARY_ID = DISEASE_ACCESSION

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
    """
    Enum of all the fields in the target-disease dataset. Used to generate the
    bulk of relationships in the graph. Values are the spellings used in the
    Open Targets parquet files.
    """

    # mandatory fields
    INTERACTION_ACCESSION = "id"

    TARGET_GENE_ENSG = "targetId"
    _PRIMARY_SOURCE_ID = TARGET_GENE_ENSG

    DISEASE_ACCESSION = "diseaseId"
    _PRIMARY_TARGET_ID = DISEASE_ACCESSION

    TYPE = "datatypeId"
    SOURCE = "datasourceId"
    LITERATURE = "literature"
    SCORE = "score"

class TargetDiseaseEvidenceAdapter:
    def __init__(
        self,
        datasets: list[TargetDiseaseDataset],
        node_fields: list[
            TargetNodeField
            | DiseaseNodeField
        ],
        target_disease_edge_fields: list[TargetDiseaseEdgeField],
        test_mode: bool = False,
    ):
        self.datasets = datasets
        self.node_fields = node_fields
        self.target_disease_edge_fields = target_disease_edge_fields
        self.test_mode = test_mode

        if self.test_mode:
            logger.warning(
                "Open Targets adapter: Test mode is enabled. "
                "Only processing 100 rows."
            )

    def download_data(self, version: str, force: bool = False):
        """
        Download datasets from Open Targets website. Manage downloading and
        caching of files. TODO

        Args:

            version: Version of the Open Targets data to download.

            force: Whether to force download of files even if they already
            exist.
        """
        pass

    def load_data(
        self,
        stats: bool = False,
        show_nodes: bool = False,
        show_edges: bool = False,
    ):
        """
        Load data from disk into Spark DataFrames.

        Args:

            stats: Whether to print out schema and counts of nodes and edges.

            show_nodes: Whether to print out the first row of each node
            dataframe.

            show_edges: Whether to print out the first row of each edge
            dataframe.
        """

        logger.info("Loading Open Targets data from disk.")

        # Read in evidence data and target / disease annotations
        from pathlib import Path
        cwd = Path.cwd()

        evidence_path = cwd / "data/ot_files/evidence/*/*.parquet"
        self.evidence_df = evidence_df = duckdb.read_parquet(str(evidence_path))

        target_path = cwd / "data/ot_files/targets/*.parquet"
        self.target_df = target_df = duckdb.read_parquet(str(target_path))

        disease_path = cwd / "data/ot_files/diseases/*.parquet"
        self.disease_df = disease_df = duckdb.read_parquet(str(disease_path))

        if stats:
            # print schema
            print(evidence_df.columns)
            print(target_df.columns)
            print(disease_df.columns)

            dataframes = [
                "evidence_df",
                "target_df",
                "disease_df"]
            individual_queries = [f"(SELECT '{df}' AS 'Dataframe', COUNT(*) AS 'Row Count' FROM {df})" for df in dataframes]
            duckdb.sql("UNION ALL ".join(individual_queries)).show()

            # print number of rows per datasource
            duckdb.sql("SELECT datasourceId, COUNT(*) FROM evidence_df GROUP BY datasourceId").show()

    def _yield_node_type(
        self,
        df,
        node_field_type,
        ontology_class: Optional[str] = None,
    ):
        """
        Yield the node type from the dataframe.

        Args:

            df: Spark DataFrame containing the node data.

            node_field_type: Enum containing the node fields.

            ontology_class: Ontological class of the node (corresponding to the
            `label_in_input` field in the schema configuration).
        """

        fields = [field.value for field in self.node_fields if isinstance(field, node_field_type)]
        query_string = f"SELECT {','.join(fields)} FROM df"

        logger.info(f"Generating nodes of {node_field_type}.")

        if self.test_mode:
            query_string = query_string + " LIMIT 100"

        query = duckdb.sql(query_string)
        query.execute()
        index_field_dict = {i: idx for idx, i in enumerate(query.columns)}
        while True:
            row = query.fetchone()
            if row is None:
                break

            # normalize id
            _id, _type = _process_id_and_type(
                row[index_field_dict[node_field_type._PRIMARY_ID.value]], ontology_class
            )

            if not _id:
                logger.debug(f"Node <{node_field_type}> has no id. Skipping.")
                continue

            logger.debug(f"Processed {node_field_type} with id {_id} and type {_type}")

            _props = {}
            _props["version"] = "22.11"
            _props["source"] = "Open Targets"
            _props["licence"] = "https://platform-docs.opentargets.org/licence"

            for (field_name, index) in index_field_dict.items():
                _props[field_name] = row[index]

            yield (_id, _type, _props)

    def get_nodes(self):
        """
        Yield nodes from the target and disease dataframes.
        """

        # Targets
        yield from self._yield_node_type(self.target_df, TargetNodeField, "ensembl")

        # Diseases
        yield from self._yield_node_type(self.disease_df, DiseaseNodeField)

    def get_edges(self):
        yield from self._process_gene_disease_edges(self.evidence_df)

    def _process_gene_disease_edges(self, df):
        """
        Process one batch of edges.

        Args:

            batch: Spark DataFrame containing the edges of one batch.
        """

        query_string = "SELECT * FROM df"

        if self.test_mode:
            # limit batch df to 100 rows
            query_string = query_string + " LIMIT 100"

        query = duckdb.sql(query_string)
        query.execute()
        index_field_dict = {i: idx for idx, i in enumerate(query.columns)}
        while True:
            row = query.fetchone()
            if row is None:
                break

            # collect properties from fields, skipping null values
            properties = {}
            for field in self.target_disease_edge_fields:
                # skip disease and target ids, relationship id, and datatype id
                # as they are encoded in the relationship
                if field not in [
                    TargetDiseaseEdgeField.LITERATURE,
                    TargetDiseaseEdgeField.SCORE,
                    TargetDiseaseEdgeField.SOURCE,
                ]:
                    continue

                if field == TargetDiseaseEdgeField.SOURCE:
                    properties["source"] = row[index_field_dict[field.value]]
                    properties["licence"] = _find_licence(row[index_field_dict[field.value]])
                elif row[index_field_dict[field.value]]:
                    properties[field.value] = row[index_field_dict[field.value]]

            properties["version"] = "22.11"

            disease_id, _ = _process_id_and_type(row[index_field_dict["diseaseId"]])
            gene_id, _ = _process_id_and_type(row[index_field_dict["targetId"]], "ensembl")

            edge = (
                row[index_field_dict["id"]],
                gene_id,
                disease_id,
                row[index_field_dict["datatypeId"]],
                properties,
            )

            yield edge


@functools.lru_cache()
def _process_id_and_type(inputId: str, _type: Optional[str] = None):
    """
    Process diseaseId and diseaseType fields from evidence data. Process
    gene (ENSG) ids.

    Args:

        inputId: id of the node.

        _type: type of the node.
    """

    if not inputId:
        return (None, None)

    _id = None

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

    if not _id:
        return (None, None)

    return (_id, _type)


def _find_licence(source: str) -> str:
    """
    Find and return the licence for a source.

    Args:

        source: source of the evidence. Spelling as in the Open Targets
        evidence data.
    """
    return _licences.get(source, "Unknown")
