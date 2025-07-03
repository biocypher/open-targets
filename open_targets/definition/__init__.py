"""Collection of predefined node and edge definitions for Open Targets data.

This module provides ready-to-use definitions for various biological entities
(nodes) and their relationships (edges) in the Open Targets data. These
definitions can be imported and used directly or easily derived following
Python's dataclass practices.
"""

from open_targets.definition.edge_disease_biomarker import edge_disease_biomarker_gene_expression, edge_disease_biomarker_genetic_variation
from open_targets.definition.edge_disease_has_child import edge_disease_has_child
from open_targets.definition.edge_disease_has_synonym import edge_disease_has_broad_synonym, edge_disease_has_exact_synonym, edge_disease_has_narrow_synonym, edge_disease_has_related_synonym
from open_targets.definition.edge_disease_has_xref import edge_disease_has_xref
from open_targets.definition.edge_disease_is_a import edge_disease_is_a
from open_targets.definition.edge_disease_phenotype import edge_disease_phenotype
from open_targets.definition.edge_evidence_has_drug_response import edge_evidence_has_drug_response
from open_targets.definition.edge_evidence_has_mutated_sample import edge_evidence_has_mutated_sample
from open_targets.definition.edge_evidence_has_text_mining_sentence import edge_evidence_has_text_mining_sentence
from open_targets.definition.edge_evidence_has_url import edge_evidence_has_url
from open_targets.definition.edge_evidence_has_variant import edge_evidence_has_variant
from open_targets.definition.edge_molecule_adverse_reaction import edge_molecule_adverse_reaction
from open_targets.definition.edge_molecule_disease import edge_molecule_disease
from open_targets.definition.edge_molecule_drug_warning import edge_molecule_drug_warning
from open_targets.definition.edge_molecule_has_child import edge_molecule_has_child
from open_targets.definition.edge_molecule_has_synonym import edge_molecule_has_synonym
from open_targets.definition.edge_molecule_has_xref import edge_molecule_has_xref
from open_targets.definition.edge_molecule_linked_disease import edge_molecule_linked_disease
from open_targets.definition.edge_molecule_linked_target import edge_molecule_linked_target
from open_targets.definition.edge_molecule_target import edge_molecule_target
from open_targets.definition.edge_target_adverse_reaction import edge_target_adverse_reaction
from open_targets.definition.edge_target_biomarker import edge_target_biomarker_gene_expression, edge_target_biomarker_genetic_variation
from open_targets.definition.edge_target_disease import edge_target_disease
from open_targets.definition.edge_target_disease_aotf import edge_target_disease_aotf
from open_targets.definition.edge_target_disease_association_by_datasource_direct import edge_target_disease_association_by_datasource_direct
from open_targets.definition.edge_target_disease_association_by_datasource_indirect import edge_target_disease_association_by_datasource_indirect
from open_targets.definition.edge_target_disease_association_by_datatype_direct import edge_target_disease_association_by_datatype_direct
from open_targets.definition.edge_target_disease_association_by_datatype_indirect import edge_target_disease_association_by_datatype_indirect
from open_targets.definition.edge_target_disease_association_by_overall_direct import edge_target_disease_association_by_overall_direct
from open_targets.definition.edge_target_disease_association_by_overall_indirect import edge_target_disease_association_by_overall_indirect
from open_targets.definition.edge_target_disease_ebisearch import edge_target_disease_ebisearch
from open_targets.definition.edge_target_disease_evidence_ebisearch import edge_target_disease_evidence_ebisearch
from open_targets.definition.edge_target_go import edge_target_go
from open_targets.definition.edge_target_pathway import edge_target_pathway
from open_targets.definition.edge_target_target import edge_target_target
from open_targets.definition.edge_target_tissue_expression import edge_target_tissue_expression
from open_targets.definition.node_biomarker import node_biomarker_gene_expression, node_biomarker_genetic_variation
from open_targets.definition.node_clinical_trial import node_clinical_trial
from open_targets.definition.node_cross_reference import node_disease_cross_reference, node_molecule_cross_reference
from open_targets.definition.node_disease import node_diseases
from open_targets.definition.node_drug_response import node_drug_response
from open_targets.definition.node_gene_ontology import node_gene_ontology
from open_targets.definition.node_molecule import node_molecule
from open_targets.definition.node_mouse_model import node_mouse_model
from open_targets.definition.node_mouse_phenotype import node_mouse_phenotype
from open_targets.definition.node_mouse_target import node_mouse_target
from open_targets.definition.node_mutated_sample import node_mutated_sample
from open_targets.definition.node_pathway import node_pathway
from open_targets.definition.node_phenotype import node_phenotype
from open_targets.definition.node_synonym import node_disease_synonym_broad, node_disease_synonym_exact, node_disease_synonym_narrow, node_disease_synonym_related, node_molecule_synonym
from open_targets.definition.node_target import node_targets
from open_targets.definition.node_text_mining_sentence import node_text_mining_sentence
from open_targets.definition.node_tissue import node_tissue
from open_targets.definition.node_url import node_url
from open_targets.definition.node_variant import node_variant

from open_targets.definition.edge_disease_biomarker import edge_disease_biomarker_gene_expression, edge_disease_biomarker_genetic_variation
from open_targets.definition.edge_disease_has_child import edge_disease_has_child
from open_targets.definition.edge_disease_has_synonym import edge_disease_has_broad_synonym, edge_disease_has_exact_synonym, edge_disease_has_narrow_synonym, edge_disease_has_related_synonym
from open_targets.definition.edge_disease_has_xref import edge_disease_has_xref
from open_targets.definition.edge_disease_is_a import edge_disease_is_a
from open_targets.definition.edge_disease_phenotype import edge_disease_phenotype
from open_targets.definition.edge_evidence_has_drug_response import edge_evidence_has_drug_response
from open_targets.definition.edge_evidence_has_mutated_sample import edge_evidence_has_mutated_sample
from open_targets.definition.edge_evidence_has_text_mining_sentence import edge_evidence_has_text_mining_sentence
from open_targets.definition.edge_evidence_has_url import edge_evidence_has_url
from open_targets.definition.edge_evidence_has_variant import edge_evidence_has_variant
from open_targets.definition.edge_molecule_adverse_reaction import edge_molecule_adverse_reaction
from open_targets.definition.edge_molecule_disease import edge_molecule_disease
from open_targets.definition.edge_molecule_drug_warning import edge_molecule_drug_warning
from open_targets.definition.edge_molecule_has_child import edge_molecule_has_child
from open_targets.definition.edge_molecule_has_synonym import edge_molecule_has_synonym
from open_targets.definition.edge_molecule_has_xref import edge_molecule_has_xref
from open_targets.definition.edge_molecule_linked_disease import edge_molecule_linked_disease
from open_targets.definition.edge_molecule_linked_target import edge_molecule_linked_target
from open_targets.definition.edge_molecule_target import edge_molecule_target
from open_targets.definition.edge_target_adverse_reaction import edge_target_adverse_reaction
from open_targets.definition.edge_target_biomarker import edge_target_biomarker_gene_expression, edge_target_biomarker_genetic_variation
from open_targets.definition.edge_target_disease import edge_target_disease
from open_targets.definition.edge_target_disease_aotf import edge_target_disease_aotf
from open_targets.definition.edge_target_disease_association_by_datasource_direct import edge_target_disease_association_by_datasource_direct
from open_targets.definition.edge_target_disease_association_by_datasource_indirect import edge_target_disease_association_by_datasource_indirect
from open_targets.definition.edge_target_disease_association_by_datatype_direct import edge_target_disease_association_by_datatype_direct
from open_targets.definition.edge_target_disease_association_by_datatype_indirect import edge_target_disease_association_by_datatype_indirect
from open_targets.definition.edge_target_disease_association_by_overall_direct import edge_target_disease_association_by_overall_direct
from open_targets.definition.edge_target_disease_association_by_overall_indirect import edge_target_disease_association_by_overall_indirect
from open_targets.definition.edge_target_disease_ebisearch import edge_target_disease_ebisearch
from open_targets.definition.edge_target_disease_evidence_ebisearch import edge_target_disease_evidence_ebisearch
from open_targets.definition.edge_target_go import edge_target_go
from open_targets.definition.edge_target_pathway import edge_target_pathway
from open_targets.definition.edge_target_target import edge_target_target
from open_targets.definition.edge_target_tissue_expression import edge_target_tissue_expression
from open_targets.definition.node_biomarker import node_biomarker_gene_expression, node_biomarker_genetic_variation
from open_targets.definition.node_clinical_trial import node_clinical_trial
from open_targets.definition.node_cross_reference import node_disease_cross_reference, node_molecule_cross_reference
from open_targets.definition.node_disease import node_diseases
from open_targets.definition.node_drug_response import node_drug_response
from open_targets.definition.node_gene_ontology import node_gene_ontology
from open_targets.definition.node_molecule import node_molecule
from open_targets.definition.node_mouse_model import node_mouse_model
from open_targets.definition.node_mouse_phenotype import node_mouse_phenotype
from open_targets.definition.node_mouse_target import node_mouse_target
from open_targets.definition.node_mutated_sample import node_mutated_sample
from open_targets.definition.node_pathway import node_pathway
from open_targets.definition.node_phenotype import node_phenotype
from open_targets.definition.node_synonym import node_disease_synonym_broad, node_disease_synonym_exact, node_disease_synonym_narrow, node_disease_synonym_related, node_molecule_synonym
from open_targets.definition.node_target import node_targets
from open_targets.definition.node_text_mining_sentence import node_text_mining_sentence
from open_targets.definition.node_tissue import node_tissue
from open_targets.definition.node_url import node_url
from open_targets.definition.node_variant import node_variant

__all__ = [
    "edge_disease_biomarker_gene_expression",
    "edge_disease_biomarker_genetic_variation",
    "edge_disease_has_child",
    "edge_disease_has_broad_synonym",
    "edge_disease_has_exact_synonym",
    "edge_disease_has_narrow_synonym",
    "edge_disease_has_related_synonym",
    "edge_disease_has_xref",
    "edge_disease_is_a",
    "edge_disease_phenotype",
    "edge_evidence_has_drug_response",
    "edge_evidence_has_mutated_sample",
    "edge_evidence_has_text_mining_sentence",
    "edge_evidence_has_url",
    "edge_evidence_has_variant",
    "edge_molecule_adverse_reaction",
    "edge_molecule_disease",
    "edge_molecule_drug_warning",
    "edge_molecule_has_child",
    "edge_molecule_has_synonym",
    "edge_molecule_has_xref",
    "edge_molecule_linked_disease",
    "edge_molecule_linked_target",
    "edge_molecule_target",
    "edge_target_adverse_reaction",
    "edge_target_biomarker_gene_expression",
    "edge_target_biomarker_genetic_variation",
    "edge_target_disease",
    "edge_target_disease_aotf",
    "edge_target_disease_association_by_datasource_direct",
    "edge_target_disease_association_by_datasource_indirect",
    "edge_target_disease_association_by_datatype_direct",
    "edge_target_disease_association_by_datatype_indirect",
    "edge_target_disease_association_by_overall_direct",
    "edge_target_disease_association_by_overall_indirect",
    "edge_target_disease_ebisearch",
    "edge_target_disease_evidence_ebisearch",
    "edge_target_go",
    "edge_target_pathway",
    "edge_target_target",
    "edge_target_tissue_expression",
    "node_biomarker_gene_expression",
    "node_biomarker_genetic_variation",
    "node_clinical_trial",
    "node_cross_reference",
    "node_disease_cross_reference",
    "node_drug_response",
    "node_molecule_cross_reference",
    "node_diseases",
    "node_gene_ontology",
    "node_molecule",
    "node_mouse_model",
    "node_mouse_phenotype",
    "node_mouse_target",
    "node_mutated_sample",
    "node_pathway",
    "node_phenotype",
    "node_disease_synonym_broad",
    "node_disease_synonym_exact",
    "node_disease_synonym_narrow",
    "node_disease_synonym_related",
    "node_molecule_synonym",
    "node_targets",
    "node_text_mining_sentence",
    "node_tissue",
    "node_url",
    "node_variant",
]
