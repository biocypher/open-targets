"""A pipeline to build Open Targets platform data as a BioCypher KG."""

from biocypher import BioCypher

from open_targets.adapter.context import GenerationContext
from open_targets.definition import (
    edge_target_disease,
    edge_target_go,
    node_diseases,
    node_gene_ontology,
    node_molecule,
    node_mouse_phenotype,
    node_mouse_target,
    node_targets,
)


def main():
    """Run the import using BioCypher and the Open Targets adapter."""
    # Start BioCypher
    bc = BioCypher(
        biocypher_config_path="config/biocypher_config.yaml",
    )

    # Check the schema
    bc.show_ontology_structure()

    node_definitions = [
        node_targets,
        node_diseases,
        node_molecule,
        node_gene_ontology,
        node_mouse_phenotype,
        node_mouse_target,
    ]
    edge_definitions = [edge_target_disease, edge_target_go]

    # Open Targets
    context = GenerationContext(
        node_definitions=node_definitions,
        edge_definitions=edge_definitions,
        datasets_location="data/ot_files",
        limit=100,
    )

    for node_definition in node_definitions:
        bc.write_nodes(context.get_generator(node_definition))
    for edge_definition in edge_definitions:
        bc.write_edges(context.get_generator(edge_definition))

    # Post import functions
    bc.write_import_call()
    bc.summary()


if __name__ == "__main__":
    main()
