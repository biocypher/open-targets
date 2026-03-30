"""Summary: shared expressions for stable IDs/values across definitions.

These helpers build stable primary IDs (namespaced strings or hashes) and
normalized values used across node/edge definitions, especially where source
datasets lack explicit primary keys or have inconsistent identifier formats.
"""

from open_targets.definition.reference_kg.expression.adverse_reaction_primary_id_expression import (
    adverse_reaction_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.colocalisation_primary_id_expression import (
    colocalisation_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.database_cross_reference_disease_primary_id_expression import (
    database_cross_reference_disease_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.database_cross_reference_hpo_primary_id_expression import (
    database_cross_reference_hpo_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.database_cross_reference_target_primary_id_expression import (
    database_cross_reference_target_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.database_cross_reference_target_value_expression import (
    database_cross_reference_target_value_expression,
)
from open_targets.definition.reference_kg.expression.disease_phenotype_association_primary_id_expression import (
    disease_phenotype_association_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.disease_synonym_broad_primary_id_expression import (
    disease_synonym_broad_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.disease_synonym_exact_primary_id_expression import (
    disease_synonym_exact_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.disease_synonym_narrow_primary_id_expression import (
    disease_synonym_narrow_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.disease_synonym_related_primary_id_expression import (
    disease_synonym_related_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.drug_warning_primary_id_expression import (
    drug_warning_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.genetic_association_study_literature_entry_expression import (
    genetic_association_study_literature_entry_expression,
)
from open_targets.definition.reference_kg.expression.literature_entry_primary_id_expression import (
    literature_entry_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.mechanism_of_action_primary_id_expression import (
    mechanism_of_action_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.pharmacogenomics_annotation_primary_id_expression import (
    pharmacogenomics_annotation_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.species_primary_id_expression import species_primary_id_expression
from open_targets.definition.reference_kg.expression.subcellular_location_primary_id_expression import (
    subcellular_location_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.target_classification_primary_id_expression import (
    target_classification_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.target_disease_association_literature_entry_expression import (
    target_disease_association_literature_entry_expression,
)
from open_targets.definition.reference_kg.expression.target_prioritisation_primary_id_expression import (
    target_prioritisation_primary_id_expression,
)
from open_targets.definition.reference_kg.expression.target_target_interaction_literature_entry_expression import (
    target_target_interaction_literature_entry_expression,
)
from open_targets.definition.reference_kg.expression.target_target_interaction_primary_id_expression import (
    target_target_interaction_primary_id_expression,
)

__all__ = [
    "adverse_reaction_primary_id_expression",
    "colocalisation_primary_id_expression",
    "database_cross_reference_disease_primary_id_expression",
    "database_cross_reference_hpo_primary_id_expression",
    "database_cross_reference_target_primary_id_expression",
    "database_cross_reference_target_value_expression",
    "disease_phenotype_association_primary_id_expression",
    "disease_synonym_broad_primary_id_expression",
    "disease_synonym_exact_primary_id_expression",
    "disease_synonym_narrow_primary_id_expression",
    "disease_synonym_related_primary_id_expression",
    "drug_warning_primary_id_expression",
    "genetic_association_study_literature_entry_expression",
    "literature_entry_primary_id_expression",
    "mechanism_of_action_primary_id_expression",
    "pharmacogenomics_annotation_primary_id_expression",
    "species_primary_id_expression",
    "subcellular_location_primary_id_expression",
    "target_classification_primary_id_expression",
    "target_disease_association_literature_entry_expression",
    "target_prioritisation_primary_id_expression",
    "target_target_interaction_literature_entry_expression",
    "target_target_interaction_primary_id_expression",
]
