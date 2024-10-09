# VSCode does not add the root directory to the path (by default?). Not sure why
# this works sometimes and not others. This is a workaround.
import sys

from bccb.uniprot_adapter import (
    Uniprot,
    UniprotEdgeField,
    UniprotEdgeType,
    UniprotNodeField,
    UniprotNodeType,
)
from biocypher import BioCypher
from dmb.adapter import (
    DepMapAdapter,
    DepMapCellLineNodeField,
    DepMapEdgeType,
    DepMapGeneToCellLineEdgeField,
    DepMapNodeType,
)

from otar_biocypher.target_disease_evidence_adapter import (  # MouseModelNodeField,
    DiseaseNodeField,
    GeneOntologyNodeField,
    MousePhenotypeNodeField,
    MouseTargetNodeField,
    TargetDiseaseDataset,
    TargetDiseaseEdgeField,
    TargetDiseaseEvidenceAdapter,
    TargetNodeField,
)

sys.path.append("")

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

depmap_node_types = [
    DepMapNodeType.CELL_LINE,
]

depmap_node_fields = [
    DepMapCellLineNodeField.CELL_LINE_NAME,
    DepMapCellLineNodeField.CELL_LINE_TISSUE,
    DepMapCellLineNodeField.CELL_LINE_TUMOUR_GRADE,
    DepMapCellLineNodeField.CELL_LINE_MUTATION_DATA,
    DepMapCellLineNodeField.CELL_LINE_CNV_DATA,
    # there are many more
]

depmap_edge_types = [
    DepMapEdgeType.GENE_TO_CELL_LINE,
]

depmap_edge_fields = [
    DepMapGeneToCellLineEdgeField._TRANSLATE_SOURCE_ID_TO_ENSG,
    DepMapGeneToCellLineEdgeField._PRIMARY_TARGET_ID,
    DepMapGeneToCellLineEdgeField.DEPENDENCY_SCORE_NORMALISED,
]


def main():
    """
    Main function running the import using BioCypher and the adapter.
    """

    # Start BioCypher
    bc = BioCypher(biocypher_config_path="config/biocypher_config_extended.yaml")

    # Check the schema
    bc.show_ontology_structure()

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

    # Dependency Map
    depmap_adapter = DepMapAdapter(
        node_types=depmap_node_types,
        node_fields=depmap_node_fields,
        edge_types=depmap_edge_types,
        edge_fields=depmap_edge_fields,
        test_mode=True,
    )

    # Write nodes
    # bc.write_nodes(target_disease_adapter.get_nodes())
    bc.write_nodes(uniprot_adapter.get_nodes())
    bc.write_nodes(depmap_adapter.get_nodes())

    # Write edges
    bc.write_edges(uniprot_adapter.get_edges())
    bc.write_edges(depmap_adapter.get_edges())

    # Write OTAR edges in batches to avoid memory issues
    batches = target_disease_adapter.get_edge_batches()
    for batch in batches:
        bc.write_edges(target_disease_adapter.get_edges(batch_number=batch))

    # Post import functions
    bc.write_import_call()
    bc.summary()


if __name__ == "__main__":
    main()
