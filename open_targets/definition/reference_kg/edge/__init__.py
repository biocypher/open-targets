"""Summary: edge definitions for the reference knowledge graph."""

from open_targets.definition.reference_kg.edge.edge_biosample_is_a_biosample import edge_biosample_is_a_biosample
from open_targets.definition.reference_kg.edge.edge_cell_line_sampled_from_tissue import (
    edge_cell_line_sampled_from_tissue,
)
from open_targets.definition.reference_kg.edge.edge_colocalisation_compares_signal_credible_set_left import (
    edge_colocalisation_compares_signal_credible_set_left,
)
from open_targets.definition.reference_kg.edge.edge_colocalisation_compares_signal_credible_set_right import (
    edge_colocalisation_compares_signal_credible_set_right,
)
from open_targets.definition.reference_kg.edge.edge_credible_set_contains_variant_variant import (
    edge_credible_set_contains_variant_variant,
)
from open_targets.definition.reference_kg.edge.edge_credible_set_predicts_target_target import (
    edge_credible_set_predicts_target_target,
)
from open_targets.definition.reference_kg.edge.edge_disease_has_database_cross_reference_database_cross_reference import (
    edge_disease_has_database_cross_reference_database_cross_reference,
)
from open_targets.definition.reference_kg.edge.edge_disease_has_synonym_synonym_broad import (
    edge_disease_has_synonym_synonym_broad,
)
from open_targets.definition.reference_kg.edge.edge_disease_has_synonym_synonym_exact import (
    edge_disease_has_synonym_synonym_exact,
)
from open_targets.definition.reference_kg.edge.edge_disease_has_synonym_synonym_narrow import (
    edge_disease_has_synonym_synonym_narrow,
)
from open_targets.definition.reference_kg.edge.edge_disease_has_synonym_synonym_related import (
    edge_disease_has_synonym_synonym_related,
)
from open_targets.definition.reference_kg.edge.edge_disease_is_a_disease import edge_disease_is_a_disease
from open_targets.definition.reference_kg.edge.edge_disease_phenotype_association_has_object_phenotype import (
    edge_disease_phenotype_association_has_object_phenotype,
)
from open_targets.definition.reference_kg.edge.edge_disease_subject_of_disease_phenotype_association import (
    edge_disease_subject_of_disease_phenotype_association,
)
from open_targets.definition.reference_kg.edge.edge_genetic_association_study_has_credible_set_credible_set import (
    edge_genetic_association_study_has_credible_set_credible_set,
)
from open_targets.definition.reference_kg.edge.edge_genetic_association_study_measured_in_biosample import (
    edge_genetic_association_study_measured_in_biosample,
)
from open_targets.definition.reference_kg.edge.edge_genetic_association_study_published_in_literature_entry import (
    edge_genetic_association_study_published_in_literature_entry,
)
from open_targets.definition.reference_kg.edge.edge_genetic_association_study_reports_trait_disease import (
    edge_genetic_association_study_reports_trait_disease,
)
from open_targets.definition.reference_kg.edge.edge_genetic_association_study_reports_trait_target import (
    edge_genetic_association_study_reports_trait_target,
)
from open_targets.definition.reference_kg.edge.edge_literature_mentions_entity import edge_literature_mentions_entity
from open_targets.definition.reference_kg.edge.edge_mechanism_of_action_has_target_target import (
    edge_mechanism_of_action_has_target_target,
)
from open_targets.definition.reference_kg.edge.edge_molecule_derived_from_molecule import (
    edge_molecule_derived_from_molecule,
)
from open_targets.definition.reference_kg.edge.edge_molecule_has_adverse_reaction_adverse_reaction import (
    edge_molecule_has_adverse_reaction_adverse_reaction,
)
from open_targets.definition.reference_kg.edge.edge_molecule_has_drug_warning import edge_molecule_has_drug_warning
from open_targets.definition.reference_kg.edge.edge_molecule_has_mechanism_of_action import (
    edge_molecule_has_mechanism_of_action,
)
from open_targets.definition.reference_kg.edge.edge_molecule_indicates_disease import edge_molecule_indicates_disease
from open_targets.definition.reference_kg.edge.edge_mouse_gene_allele_in_mouse_model import (
    edge_mouse_gene_allele_in_mouse_model,
)
from open_targets.definition.reference_kg.edge.edge_mouse_model_has_phenotype_mouse_phenotype import (
    edge_mouse_model_has_phenotype_mouse_phenotype,
)
from open_targets.definition.reference_kg.edge.edge_mouse_model_has_phenotype_phenotype import (
    edge_mouse_model_has_phenotype_phenotype,
)
from open_targets.definition.reference_kg.edge.edge_mouse_phenotype_classified_as_mouse_phenotype_class import (
    edge_mouse_phenotype_classified_as_mouse_phenotype_class,
)
from open_targets.definition.reference_kg.edge.edge_pathway_annotated_with_disease import (
    edge_pathway_annotated_with_disease,
)
from open_targets.definition.reference_kg.edge.edge_pathway_is_part_of_pathway import edge_pathway_is_part_of_pathway
from open_targets.definition.reference_kg.edge.edge_pharmacogenomics_annotation_associated_with_disease import (
    edge_pharmacogenomics_annotation_associated_with_disease,
)
from open_targets.definition.reference_kg.edge.edge_pharmacogenomics_annotation_has_molecule import (
    edge_pharmacogenomics_annotation_has_molecule,
)
from open_targets.definition.reference_kg.edge.edge_pharmacogenomics_annotation_has_target import (
    edge_pharmacogenomics_annotation_has_target,
)
from open_targets.definition.reference_kg.edge.edge_pharmacogenomics_annotation_has_variant import (
    edge_pharmacogenomics_annotation_has_variant,
)
from open_targets.definition.reference_kg.edge.edge_pharmacogenomics_annotation_supported_by_literature_entry import (
    edge_pharmacogenomics_annotation_supported_by_literature_entry,
)
from open_targets.definition.reference_kg.edge.edge_phenotype_has_database_cross_reference_database_cross_reference import (
    edge_phenotype_has_database_cross_reference_database_cross_reference,
)
from open_targets.definition.reference_kg.edge.edge_phenotype_is_a_phenotype import edge_phenotype_is_a_phenotype
from open_targets.definition.reference_kg.edge.edge_reaction_is_part_of_pathway import edge_reaction_is_part_of_pathway
from open_targets.definition.reference_kg.edge.edge_regulatory_element_active_in_biosample import (
    edge_regulatory_element_active_in_biosample,
)
from open_targets.definition.reference_kg.edge.edge_regulatory_element_regulates_target import (
    edge_regulatory_element_regulates_target,
)
from open_targets.definition.reference_kg.edge.edge_regulatory_element_supported_by_literature_entry import (
    edge_regulatory_element_supported_by_literature_entry,
)
from open_targets.definition.reference_kg.edge.edge_target_associated_with_adverse_reaction import (
    edge_target_associated_with_adverse_reaction,
)
from open_targets.definition.reference_kg.edge.edge_target_belongs_to_target_classification import (
    edge_target_belongs_to_target_classification,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_cancer_biomarkers_has_drug_response_entity import (
    edge_target_disease_association_cancer_biomarkers_has_drug_response_entity,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_cancer_biomarkers_has_molecule_molecule import (
    edge_target_disease_association_cancer_biomarkers_has_molecule_molecule,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_cancer_biomarkers_has_object_disease import (
    edge_target_disease_association_cancer_biomarkers_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_cancer_gene_census_has_object_disease import (
    edge_target_disease_association_cancer_gene_census_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_chembl_has_molecule_molecule import (
    edge_target_disease_association_chembl_has_molecule_molecule,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_chembl_has_object_disease import (
    edge_target_disease_association_chembl_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_clingen_has_object_disease import (
    edge_target_disease_association_clingen_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_crispr_has_object_disease import (
    edge_target_disease_association_crispr_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_crispr_screen_has_object_disease import (
    edge_target_disease_association_crispr_screen_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_crispr_tested_in_cell_line import (
    edge_target_disease_association_crispr_tested_in_cell_line,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_europepmc_has_object_disease import (
    edge_target_disease_association_europepmc_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_eva_has_object_disease import (
    edge_target_disease_association_eva_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_eva_somatic_has_object_disease import (
    edge_target_disease_association_eva_somatic_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_expression_atlas_has_object_disease import (
    edge_target_disease_association_expression_atlas_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_gene2phenotype_has_object_disease import (
    edge_target_disease_association_gene2phenotype_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_gene_burden_has_object_disease import (
    edge_target_disease_association_gene_burden_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_genomics_england_has_object_disease import (
    edge_target_disease_association_genomics_england_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_gwas_credible_sets_has_object_disease import (
    edge_target_disease_association_gwas_credible_sets_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_impc_has_object_disease import (
    edge_target_disease_association_impc_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_inferred_from_mouse_model import (
    edge_target_disease_association_inferred_from_mouse_model,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_inferred_from_reaction import (
    edge_target_disease_association_inferred_from_reaction,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_intogen_has_object_disease import (
    edge_target_disease_association_intogen_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_orphanet_has_object_disease import (
    edge_target_disease_association_orphanet_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_reactome_has_object_disease import (
    edge_target_disease_association_reactome_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_supported_by_literature_entry import (
    edge_target_disease_association_supported_by_literature_entry,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_uniprot_literature_has_object_disease import (
    edge_target_disease_association_uniprot_literature_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_disease_association_uniprot_variants_has_object_disease import (
    edge_target_disease_association_uniprot_variants_has_object_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_expressed_in_biosample import (
    edge_target_expressed_in_biosample,
)
from open_targets.definition.reference_kg.edge.edge_target_has_database_cross_reference_database_cross_reference import (
    edge_target_has_database_cross_reference_database_cross_reference,
)
from open_targets.definition.reference_kg.edge.edge_target_has_homologue_in_species_species import (
    edge_target_has_homologue_in_species_species,
)
from open_targets.definition.reference_kg.edge.edge_target_has_prioritisation import edge_target_has_prioritisation
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_datasource_direct_disease import (
    edge_target_has_summary_association_by_datasource_direct_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_datasource_indirect_disease import (
    edge_target_has_summary_association_by_datasource_indirect_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_datatype_direct_disease import (
    edge_target_has_summary_association_by_datatype_direct_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_datatype_indirect_disease import (
    edge_target_has_summary_association_by_datatype_indirect_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_overall_direct_disease import (
    edge_target_has_summary_association_by_overall_direct_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_summary_association_by_overall_indirect_disease import (
    edge_target_has_summary_association_by_overall_indirect_disease,
)
from open_targets.definition.reference_kg.edge.edge_target_has_target_target_interaction_target_a import (
    edge_target_has_target_target_interaction_target_a,
)
from open_targets.definition.reference_kg.edge.edge_target_has_target_target_interaction_target_b import (
    edge_target_has_target_target_interaction_target_b,
)
from open_targets.definition.reference_kg.edge.edge_target_involves_in_pathway import edge_target_involves_in_pathway
from open_targets.definition.reference_kg.edge.edge_target_located_in_subcellular_location import (
    edge_target_located_in_subcellular_location,
)
from open_targets.definition.reference_kg.edge.edge_target_modelled_by_mouse_gene import (
    edge_target_modelled_by_mouse_gene,
)
from open_targets.definition.reference_kg.edge.edge_target_related_to_go_term import edge_target_related_to_go_term
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_cancer_biomarkers import (
    edge_target_subject_of_target_disease_association_cancer_biomarkers,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_cancer_gene_census import (
    edge_target_subject_of_target_disease_association_cancer_gene_census,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_chembl import (
    edge_target_subject_of_target_disease_association_chembl,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_clingen import (
    edge_target_subject_of_target_disease_association_clingen,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_crispr import (
    edge_target_subject_of_target_disease_association_crispr,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_crispr_screen import (
    edge_target_subject_of_target_disease_association_crispr_screen,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_europepmc import (
    edge_target_subject_of_target_disease_association_europepmc,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_eva import (
    edge_target_subject_of_target_disease_association_eva,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_eva_somatic import (
    edge_target_subject_of_target_disease_association_eva_somatic,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_expression_atlas import (
    edge_target_subject_of_target_disease_association_expression_atlas,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_gene2phenotype import (
    edge_target_subject_of_target_disease_association_gene2phenotype,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_gene_burden import (
    edge_target_subject_of_target_disease_association_gene_burden,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_genomics_england import (
    edge_target_subject_of_target_disease_association_genomics_england,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_gwas_credible_sets import (
    edge_target_subject_of_target_disease_association_gwas_credible_sets,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_impc import (
    edge_target_subject_of_target_disease_association_impc,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_intogen import (
    edge_target_subject_of_target_disease_association_intogen,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_orphanet import (
    edge_target_subject_of_target_disease_association_orphanet,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_reactome import (
    edge_target_subject_of_target_disease_association_reactome,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_uniprot_literature import (
    edge_target_subject_of_target_disease_association_uniprot_literature,
)
from open_targets.definition.reference_kg.edge.edge_target_subject_of_target_disease_association_uniprot_variants import (
    edge_target_subject_of_target_disease_association_uniprot_variants,
)
from open_targets.definition.reference_kg.edge.edge_target_target_interaction_supported_by_literature_entry import (
    edge_target_target_interaction_supported_by_literature_entry,
)

__all__ = [
    "edge_biosample_is_a_biosample",
    "edge_cell_line_sampled_from_tissue",
    "edge_colocalisation_compares_signal_credible_set_left",
    "edge_colocalisation_compares_signal_credible_set_right",
    "edge_credible_set_contains_variant_variant",
    "edge_credible_set_predicts_target_target",
    "edge_disease_has_database_cross_reference_database_cross_reference",
    "edge_disease_has_synonym_synonym_broad",
    "edge_disease_has_synonym_synonym_exact",
    "edge_disease_has_synonym_synonym_narrow",
    "edge_disease_has_synonym_synonym_related",
    "edge_disease_is_a_disease",
    "edge_disease_phenotype_association_has_object_phenotype",
    "edge_disease_subject_of_disease_phenotype_association",
    "edge_genetic_association_study_has_credible_set_credible_set",
    "edge_genetic_association_study_measured_in_biosample",
    "edge_genetic_association_study_published_in_literature_entry",
    "edge_genetic_association_study_reports_trait_disease",
    "edge_genetic_association_study_reports_trait_target",
    "edge_literature_mentions_entity",
    "edge_mechanism_of_action_has_target_target",
    "edge_molecule_derived_from_molecule",
    "edge_molecule_has_adverse_reaction_adverse_reaction",
    "edge_molecule_has_drug_warning",
    "edge_molecule_has_mechanism_of_action",
    "edge_molecule_indicates_disease",
    "edge_mouse_gene_allele_in_mouse_model",
    "edge_mouse_model_has_phenotype_mouse_phenotype",
    "edge_mouse_model_has_phenotype_phenotype",
    "edge_mouse_phenotype_classified_as_mouse_phenotype_class",
    "edge_pathway_annotated_with_disease",
    "edge_pathway_is_part_of_pathway",
    "edge_pharmacogenomics_annotation_associated_with_disease",
    "edge_pharmacogenomics_annotation_has_molecule",
    "edge_pharmacogenomics_annotation_has_target",
    "edge_pharmacogenomics_annotation_has_variant",
    "edge_pharmacogenomics_annotation_supported_by_literature_entry",
    "edge_phenotype_has_database_cross_reference_database_cross_reference",
    "edge_phenotype_is_a_phenotype",
    "edge_reaction_is_part_of_pathway",
    "edge_regulatory_element_active_in_biosample",
    "edge_regulatory_element_regulates_target",
    "edge_regulatory_element_supported_by_literature_entry",
    "edge_target_associated_with_adverse_reaction",
    "edge_target_belongs_to_target_classification",
    "edge_target_disease_association_cancer_biomarkers_has_drug_response_entity",
    "edge_target_disease_association_cancer_biomarkers_has_molecule_molecule",
    "edge_target_disease_association_cancer_biomarkers_has_object_disease",
    "edge_target_disease_association_cancer_gene_census_has_object_disease",
    "edge_target_disease_association_chembl_has_molecule_molecule",
    "edge_target_disease_association_chembl_has_object_disease",
    "edge_target_disease_association_clingen_has_object_disease",
    "edge_target_disease_association_crispr_has_object_disease",
    "edge_target_disease_association_crispr_screen_has_object_disease",
    "edge_target_disease_association_crispr_tested_in_cell_line",
    "edge_target_disease_association_europepmc_has_object_disease",
    "edge_target_disease_association_eva_has_object_disease",
    "edge_target_disease_association_eva_somatic_has_object_disease",
    "edge_target_disease_association_expression_atlas_has_object_disease",
    "edge_target_disease_association_gene2phenotype_has_object_disease",
    "edge_target_disease_association_gene_burden_has_object_disease",
    "edge_target_disease_association_genomics_england_has_object_disease",
    "edge_target_disease_association_gwas_credible_sets_has_object_disease",
    "edge_target_disease_association_impc_has_object_disease",
    "edge_target_disease_association_inferred_from_mouse_model",
    "edge_target_disease_association_inferred_from_reaction",
    "edge_target_disease_association_intogen_has_object_disease",
    "edge_target_disease_association_orphanet_has_object_disease",
    "edge_target_disease_association_reactome_has_object_disease",
    "edge_target_disease_association_supported_by_literature_entry",
    "edge_target_disease_association_uniprot_literature_has_object_disease",
    "edge_target_disease_association_uniprot_variants_has_object_disease",
    "edge_target_expressed_in_biosample",
    "edge_target_has_database_cross_reference_database_cross_reference",
    "edge_target_has_homologue_in_species_species",
    "edge_target_has_prioritisation",
    "edge_target_has_summary_association_by_datasource_direct_disease",
    "edge_target_has_summary_association_by_datasource_indirect_disease",
    "edge_target_has_summary_association_by_datatype_direct_disease",
    "edge_target_has_summary_association_by_datatype_indirect_disease",
    "edge_target_has_summary_association_by_overall_direct_disease",
    "edge_target_has_summary_association_by_overall_indirect_disease",
    "edge_target_has_target_target_interaction_target_a",
    "edge_target_has_target_target_interaction_target_b",
    "edge_target_involves_in_pathway",
    "edge_target_located_in_subcellular_location",
    "edge_target_modelled_by_mouse_gene",
    "edge_target_related_to_go_term",
    "edge_target_subject_of_target_disease_association_cancer_biomarkers",
    "edge_target_subject_of_target_disease_association_cancer_gene_census",
    "edge_target_subject_of_target_disease_association_chembl",
    "edge_target_subject_of_target_disease_association_clingen",
    "edge_target_subject_of_target_disease_association_crispr",
    "edge_target_subject_of_target_disease_association_crispr_screen",
    "edge_target_subject_of_target_disease_association_europepmc",
    "edge_target_subject_of_target_disease_association_eva",
    "edge_target_subject_of_target_disease_association_eva_somatic",
    "edge_target_subject_of_target_disease_association_expression_atlas",
    "edge_target_subject_of_target_disease_association_gene2phenotype",
    "edge_target_subject_of_target_disease_association_gene_burden",
    "edge_target_subject_of_target_disease_association_genomics_england",
    "edge_target_subject_of_target_disease_association_gwas_credible_sets",
    "edge_target_subject_of_target_disease_association_impc",
    "edge_target_subject_of_target_disease_association_intogen",
    "edge_target_subject_of_target_disease_association_orphanet",
    "edge_target_subject_of_target_disease_association_reactome",
    "edge_target_subject_of_target_disease_association_uniprot_literature",
    "edge_target_subject_of_target_disease_association_uniprot_variants",
    "edge_target_target_interaction_supported_by_literature_entry",
]
