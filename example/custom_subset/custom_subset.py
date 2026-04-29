# type: ignore[reportUnknownMemberType]
"""Example: Building a knowledge graph with a custom subset of definitions.

This example demonstrates how to select specific node and edge definitions
from the reference knowledge graph to build a smaller, focused knowledge graph.
"""

import itertools

from biocypher import BioCypher

from open_targets.adapter.context import AcquisitionContext
from open_targets.definition.reference_kg.edge import (
    edge_molecule_indicates_disease,
    edge_target_has_summary_association_by_overall_direct_disease,
)
from open_targets.definition.reference_kg.node import (
    node_disease,
    node_molecule,
    node_target,
)


def main() -> None:
    """Build a knowledge graph with a custom subset of definitions."""
    # Initialize BioCypher
    biocypher_instance = BioCypher(biocypher_config_path="example/custom_subset/biocypher_config.yaml")

    # Define your custom set of definitions
    node_definitions = [
        node_target,
        node_disease,
        node_molecule,
    ]

    edge_definitions = [
        edge_target_has_summary_association_by_overall_direct_disease,
        edge_molecule_indicates_disease,
    ]

    # Create acquisition context
    context = AcquisitionContext(
        node_definitions=node_definitions,
        edge_definitions=edge_definitions,
        datasets_location="datasets",  # directory containing the downloaded datasets
        limit=100,
    )

    count = 1
    # Stream nodes and edges to BioCypher
    for node_definition in node_definitions:
        print(f"{count}: {node_definition.label}")  # noqa: T201
        count += 1
        try:
            iterable = context.get_acquisition_generator(node_definition)
            first = next(iterable)
        except StopIteration:
            continue
        else:
            iterable = itertools.chain([first], iterable)
        biocypher_instance.write_nodes(iterable)
    for edge_definition in edge_definitions:
        print(f"{count}: {edge_definition.label}")  # noqa: T201
        count += 1
        try:
            iterable = context.get_acquisition_generator(edge_definition)
            first = next(iterable)
        except StopIteration:
            continue
        else:
            iterable = itertools.chain([first], iterable)
        biocypher_instance.write_edges(iterable)

    # Finalize
    biocypher_instance.write_import_call()
    biocypher_instance.write_schema_info()
    biocypher_instance.summary()


if __name__ == "__main__":
    main()
