"""Summary: node definitions for the reference knowledge graph."""

from open_targets.definition.reference_kg.node.node_adverse_reaction import node_adverse_reaction
from open_targets.definition.reference_kg.node.node_biosample import node_biosample
from open_targets.definition.reference_kg.node.node_cell_line import node_cell_line
from open_targets.definition.reference_kg.node.node_colocalisation import node_colocalisation
from open_targets.definition.reference_kg.node.node_credible_set import node_credible_set
from open_targets.definition.reference_kg.node.node_database_cross_reference_disease import (
    node_database_cross_reference_disease,
)
from open_targets.definition.reference_kg.node.node_database_cross_reference_hpo import (
    node_database_cross_reference_hpo,
)
from open_targets.definition.reference_kg.node.node_database_cross_reference_target import (
    node_database_cross_reference_target,
)
from open_targets.definition.reference_kg.node.node_disease import node_disease
from open_targets.definition.reference_kg.node.node_disease_phenotype_association import (
    node_disease_phenotype_association,
)
from open_targets.definition.reference_kg.node.node_disease_synonym_broad import node_disease_synonym_broad
from open_targets.definition.reference_kg.node.node_disease_synonym_exact import node_disease_synonym_exact
from open_targets.definition.reference_kg.node.node_disease_synonym_narrow import node_disease_synonym_narrow
from open_targets.definition.reference_kg.node.node_disease_synonym_related import node_disease_synonym_related
from open_targets.definition.reference_kg.node.node_drug_warning import node_drug_warning
from open_targets.definition.reference_kg.node.node_genetic_association_study import node_genetic_association_study
from open_targets.definition.reference_kg.node.node_go_term import node_go_term
from open_targets.definition.reference_kg.node.node_literature_entry import node_literature_entry
from open_targets.definition.reference_kg.node.node_mechanism_of_action import node_mechanism_of_action
from open_targets.definition.reference_kg.node.node_molecule import node_molecule
from open_targets.definition.reference_kg.node.node_mouse_gene import node_mouse_gene
from open_targets.definition.reference_kg.node.node_mouse_model import node_mouse_model
from open_targets.definition.reference_kg.node.node_mouse_phenotype import node_mouse_phenotype
from open_targets.definition.reference_kg.node.node_mouse_phenotype_class import node_mouse_phenotype_class
from open_targets.definition.reference_kg.node.node_pathway import node_pathway
from open_targets.definition.reference_kg.node.node_pharmacogenomics_annotation import node_pharmacogenomics_annotation
from open_targets.definition.reference_kg.node.node_phenotype import node_phenotype
from open_targets.definition.reference_kg.node.node_reaction import node_reaction
from open_targets.definition.reference_kg.node.node_regulatory_element import node_regulatory_element
from open_targets.definition.reference_kg.node.node_so_term import node_so_term
from open_targets.definition.reference_kg.node.node_species import node_species
from open_targets.definition.reference_kg.node.node_subcellular_location import node_subcellular_location
from open_targets.definition.reference_kg.node.node_target import node_target
from open_targets.definition.reference_kg.node.node_target_classification import node_target_classification
from open_targets.definition.reference_kg.node.node_target_disease_association_cancer_biomarkers import (
    node_target_disease_association_cancer_biomarkers,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_cancer_gene_census import (
    node_target_disease_association_cancer_gene_census,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_chembl import (
    node_target_disease_association_chembl,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_clingen import (
    node_target_disease_association_clingen,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_crispr import (
    node_target_disease_association_crispr,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_crispr_screen import (
    node_target_disease_association_crispr_screen,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_europepmc import (
    node_target_disease_association_europepmc,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_eva import (
    node_target_disease_association_eva,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_eva_somatic import (
    node_target_disease_association_eva_somatic,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_expression_atlas import (
    node_target_disease_association_expression_atlas,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_gene2phenotype import (
    node_target_disease_association_gene2phenotype,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_gene_burden import (
    node_target_disease_association_gene_burden,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_genomics_england import (
    node_target_disease_association_genomics_england,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_gwas_credible_sets import (
    node_target_disease_association_gwas_credible_sets,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_impc import (
    node_target_disease_association_impc,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_intogen import (
    node_target_disease_association_intogen,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_orphanet import (
    node_target_disease_association_orphanet,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_reactome import (
    node_target_disease_association_reactome,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_uniprot_literature import (
    node_target_disease_association_uniprot_literature,
)
from open_targets.definition.reference_kg.node.node_target_disease_association_uniprot_variants import (
    node_target_disease_association_uniprot_variants,
)
from open_targets.definition.reference_kg.node.node_target_prioritisation import node_target_prioritisation
from open_targets.definition.reference_kg.node.node_target_target_interaction import node_target_target_interaction
from open_targets.definition.reference_kg.node.node_tissue import node_tissue
from open_targets.definition.reference_kg.node.node_variant import node_variant

__all__ = [
    "node_adverse_reaction",
    "node_biosample",
    "node_cell_line",
    "node_colocalisation",
    "node_credible_set",
    "node_database_cross_reference_disease",
    "node_database_cross_reference_hpo",
    "node_database_cross_reference_target",
    "node_disease",
    "node_disease_phenotype_association",
    "node_disease_synonym_broad",
    "node_disease_synonym_exact",
    "node_disease_synonym_narrow",
    "node_disease_synonym_related",
    "node_drug_warning",
    "node_genetic_association_study",
    "node_go_term",
    "node_literature_entry",
    "node_mechanism_of_action",
    "node_molecule",
    "node_mouse_gene",
    "node_mouse_model",
    "node_mouse_phenotype",
    "node_mouse_phenotype_class",
    "node_pathway",
    "node_pharmacogenomics_annotation",
    "node_phenotype",
    "node_reaction",
    "node_regulatory_element",
    "node_so_term",
    "node_species",
    "node_subcellular_location",
    "node_target",
    "node_target_classification",
    "node_target_disease_association_cancer_biomarkers",
    "node_target_disease_association_cancer_gene_census",
    "node_target_disease_association_chembl",
    "node_target_disease_association_clingen",
    "node_target_disease_association_crispr",
    "node_target_disease_association_crispr_screen",
    "node_target_disease_association_europepmc",
    "node_target_disease_association_eva",
    "node_target_disease_association_eva_somatic",
    "node_target_disease_association_expression_atlas",
    "node_target_disease_association_gene2phenotype",
    "node_target_disease_association_gene_burden",
    "node_target_disease_association_genomics_england",
    "node_target_disease_association_gwas_credible_sets",
    "node_target_disease_association_impc",
    "node_target_disease_association_intogen",
    "node_target_disease_association_orphanet",
    "node_target_disease_association_reactome",
    "node_target_disease_association_uniprot_literature",
    "node_target_disease_association_uniprot_variants",
    "node_target_prioritisation",
    "node_target_target_interaction",
    "node_tissue",
    "node_variant",
]
