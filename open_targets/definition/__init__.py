"""Collection of predefined node and edge definitions for Open Targets data.

This module provides ready-to-use definitions for various biological entities
(nodes) and their relationships (edges) in the Open Targets data. These
definitions can be imported and used directly or easily derived following
Python's dataclass practices.

Knowledge Graph Design:

Nodes:
- AdverseReaction: Represents adverse drug or target reactions (MedDRA codes).
- Annotation: Represents annotations from literature (EPMC).
- BiologicalModel: Represents biological models used in evidence.
- Biomarker: Represents gene expression or genetic variation biomarkers.
- Category: Represents categories for diseases, drugs, or targets.
- CellLine: Represents cell lines used in evidence.
- ChemicalProbe: Represents chemical probes for targets.
- ClinicalTrial: Represents clinical trials.
- CrossReference: Represents cross-references to external databases.
- Datasource: Represents data sources.
- Datatype: Represents data types.
- Disease: Represents diseases or phenotypes.
- DrugIndication: Represents drug indications.
- DrugResponse: Represents drug responses.
- GeneEssentialityMeasurement: Represents gene essentiality measurements.
- GoTerm: Represents Gene Ontology terms.
- Hallmark: Represents cancer hallmarks.
- Homologue: Represents homologous genes in other species.
- HpoTerm: Represents Human Phenotype Ontology terms.
- Indication: Represents approved and investigational drug indications.
- InteractionEvidence: Represents experimental evidence for molecular interactions.
- Keyword: Represents keywords identified in literature.
- LiteratureEntry: Represents literature entries (PubMed, PMC).
- MechanismOfAction: Represents drug mechanisms of action.
- Molecule: Represents drug or clinical candidate molecules.
- MouseModel: Represents mouse models.
- MousePhenotype: Represents mouse phenotypes.
- MouseTarget: Represents mouse targets.
- MutatedSample: Represents mutated samples.
- ObsoleteTerm: Represents obsolete terms.
- Pathway: Represents biological pathways.
- PharmacogenomicsDrug: Represents drugs in pharmacogenomics studies.
- PharmacogenomicsEvidence: Represents pharmacogenomics evidence.
- Phenotype: Represents clinical signs and symptoms.
- ProteinId: Represents protein identifiers.
- ReactomePathway: Represents Reactome pathways.
- Reference: Represents references or citations.
- SafetyLiability: Represents safety liabilities associated with targets.
- Species: Represents biological species.
- SubcellularLocation: Represents subcellular locations of proteins.
- Synonym: Represents synonymous terms.
- Target: Represents drug targets (genes/proteins).
- TargetClass: Represents classification categories for targets.
- TargetXref: Represents target cross-references.
- TepInformation: Represents Target Enabling Package (TEP) information.
- TextMiningSentence: Represents text-mined sentences supporting relationships.
- TherapeuticArea: Represents major therapeutic areas.
- Tissue: Represents tissues with expression data.
- TractabilityInfo: Represents tractability information for targets.
- Url: Represents URLs to external resources.
- Variant: Represents genetic variants.

Edges:
- ABOUT_DRUG: Links pharmacogenomics evidence to drugs.
- ABOUT_PHENOTYPE: Links pharmacogenomics evidence to phenotypes.
- ABOUT_TARGET: Links pharmacogenomics evidence to targets.
- ABOUT_VARIANT: Links pharmacogenomics evidence to variants.
- ANNOTATION_HAS_TAG: Links annotations to tags.
- BELONGS_TO_CLASS: Links targets to target classes.
- DISEASE_HAS_BIOMARKER: Links diseases to biomarkers.
- DISEASE_HAS_CATEGORY: Links diseases to categories.
- DISEASE_HAS_CHILD: Links diseases to their child terms.
- DISEASE_HAS_DATASOURCE: Links diseases to datasources.
- DISEASE_HAS_KEYWORD: Links diseases to keywords.
- DISEASE_HAS_XREF: Links diseases to cross-references.
- DISEASE_IS_A: Links diseases to their parent terms.
- DISEASE_TO_PHENOTYPE_ASSOCIATION: Links diseases to phenotypes.
- DRUG_HAS_INDICATION: Links drugs to their indications.
- DRUG_HAS_KEYWORD: Links drugs to keywords.
- DRUG_TARGETS_DISEASE: Links drugs to diseases they target.
- EDGE_DISEASE_HAS_BROAD_SYNONYM: Links diseases to their broad synonyms.
- EDGE_DISEASE_HAS_EXACT_SYNONYM: Links diseases to their exact synonyms.
- EDGE_DISEASE_HAS_NARROW_SYNONYM: Links diseases to their narrow synonyms.
- EDGE_DISEASE_HAS_RELATED_SYNONYM: Links diseases to their related synonyms.
- FROM_BIOLOGICAL_MODEL: Links evidence to biological models.
- FROM_CELL_LINE: Links evidence to cell lines.
- HAS_CHEMICAL_PROBE: Links targets to chemical probes.
- HAS_DRUG_RESPONSE: Links evidence to drug responses.
- HAS_ESSENTIALITY: Links targets to gene essentiality measurements.
- HAS_HALLMARK: Links targets to cancer hallmarks.
- HAS_HOMOLOGUE: Links targets to homologous genes.
- HAS_INTERACTION_EVIDENCE: Links target-target associations to interaction evidence.
- HAS_LITERATURE: Links evidence or pharmacogenomics evidence to literature entries.
- HAS_MUTATED_SAMPLE: Links evidence to mutated samples.
- HAS_PROTEIN_ID: Links targets to protein identifiers.
- HAS_REFERENCE: Links disease-phenotype evidence or indications or mechanisms to references.
- HAS_SAFETY_LIABILITY: Links targets to safety liabilities.
- HAS_SUBCELLULAR_LOCATION: Links targets to subcellular locations.
- HAS_SYNONYM: Links molecules to their synonyms.
- HAS_TEP_INFO: Links targets to TEP information.
- HAS_TEXT_MINING_SENTENCE: Links evidence to text mining sentences.
- HAS_TRACTABILITY_INFO: Links targets to tractability information.
- HAS_URL: Links evidence to URLs.
- HAS_VARIANT: Links evidence to variants.
- HPO_HAS_OBSOLETE_TERM: Links HPO terms to their obsolete terms.
- HPO_HAS_XREF: Links HPO terms to cross-references.
- HPO_IS_A: Links HPO terms to their parent terms.
- INTERACTS_IN_SPECIES: Links interactions to species.
- IS_IN_THERAPEUTIC_AREA: Links diseases to therapeutic areas.
- KEYWORD_COOCCURRENCE: Links co-occurring keywords.
- LINKED_TO_DISEASE: Links molecules to diseases they are associated with.
- LINKED_TO_TARGET: Links molecules to targets they are associated with.
- MECHANISM_TARGETS: Links mechanisms of action to targets.
- MENTIONS_KEYWORD: Links literature entries to keywords.
- MOLECULE_TO_ADVERSE_REACTION: Links molecules to adverse reactions.
- MOLECULE_TO_DRUG_WARNING: Links molecules to drug warnings.
- MOLECULE_TO_DISEASE_ASSOCIATION: Links molecules to diseases.
- MOLECULE_TO_TARGET_ASSOCIATION: Links molecules to targets.
- MODELS_HUMAN_TARGET: Links mouse targets to human targets.
- REACTOME_HAS_CHILD: Links Reactome pathways to their child pathways.
- REACTOME_IS_A: Links Reactome pathways to their parent pathways.
- TARGET_DISEASE_ASSOCIATION_BY_DATASOURCE_DIRECT: Links targets to diseases with direct associations by datasource.
- TARGET_DISEASE_ASSOCIATION_BY_DATASOURCE_INDIRECT: Links targets to diseases with indirect associations by datasource.
- TARGET_DISEASE_ASSOCIATION_BY_DATATYPE_DIRECT: Links targets to diseases with direct associations by datatype.
- TARGET_DISEASE_ASSOCIATION_BY_DATATYPE_INDIRECT: Links targets to diseases with indirect associations by datatype.
- TARGET_DISEASE_ASSOCIATION_BY_OVERALL_DIRECT: Links targets to diseases with direct overall associations.
- TARGET_DISEASE_ASSOCIATION_BY_OVERALL_INDIRECT: Links targets to diseases with indirect overall associations.
- TARGET_TO_ADVERSE_REACTION: Links targets to adverse reactions.
- TARGET_TO_DISEASE_ASSOCIATION: Links targets to diseases.
- TARGET_TO_DISEASE_ASSOCIATION_EBISearch: Links targets to diseases from Ebisearch Associations.
- TARGET_TO_DISEASE_EVIDENCE_EBISearch: Links targets to diseases from Ebisearch Evidence.
- TARGET_TO_GO_TERM_ASSOCIATION: Links targets to GO terms.
- TARGET_TO_TARGET_ASSOCIATION: Links targets to other targets.
- TARGET_TISSUE_EXPRESSION: Links targets to tissues based on expression data.
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
from open_targets.definition.node_datasource import node_datasource
from open_targets.definition.node_datatype import node_datatype
from open_targets.definition.node_obsolete_term import node_obsolete_term
from open_targets.definition.node_annotation import node_annotation
from open_targets.definition.node_tag import node_tag
from open_targets.definition.edge_literature_entry_has_annotation import edge_literature_entry_has_annotation
from open_targets.definition.edge_annotation_has_tag import edge_annotation_has_tag
from open_targets.definition.node_category import node_category
from open_targets.definition.edge_disease_has_category import edge_disease_has_category
from open_targets.definition.edge_target_has_category import edge_target_has_category
from open_targets.definition.edge_disease_has_datasource import edge_disease_has_datasource
from open_targets.definition.edge_target_has_datasource import edge_target_has_datasource
from open_targets.definition.edge_disease_has_keyword import edge_disease_has_keyword
from open_targets.definition.edge_drug_has_keyword import edge_drug_has_keyword
from open_targets.definition.edge_target_has_keyword import edge_target_has_keyword

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
    "node_datasource",
    "node_datatype",
    "node_obsolete_term",
    "node_annotation",
    "node_tag",
    "edge_literature_entry_has_annotation",
    "edge_annotation_has_tag",
    "node_category",
    "edge_disease_has_category",
    "edge_target_has_category",
    "edge_disease_has_datasource",
    "edge_target_has_datasource",
    "edge_disease_has_keyword",
    "edge_drug_has_keyword",
    "edge_target_has_keyword",
]
