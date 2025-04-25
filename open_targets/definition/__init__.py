"""Collection of predefined node and edge definitions for Open Targets data.

This module provides ready-to-use definitions for various biological entities
(nodes) and their relationships (edges) in the Open Targets data. These
definitions can be imported and used directly or easily derived following
Python's dataclass practices.
"""

from open_targets.definition.edge_target_disease import edge_target_disease
from open_targets.definition.edge_target_go import edge_target_go
from open_targets.definition.node_disease import node_diseases
from open_targets.definition.node_gene_ontology import node_gene_ontology
from open_targets.definition.node_molecule import node_molecule
from open_targets.definition.node_mouse_model import node_mouse_model
from open_targets.definition.node_mouse_phenotype import node_mouse_phenotype
from open_targets.definition.node_mouse_target import node_mouse_target
from open_targets.definition.node_target import node_targets

__all__ = [
    "edge_target_disease",
    "edge_target_go",
    "node_diseases",
    "node_gene_ontology",
    "node_molecule",
    "node_mouse_model",
    "node_mouse_phenotype",
    "node_mouse_target",
    "node_targets",
]
