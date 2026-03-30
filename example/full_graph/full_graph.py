# type: ignore[reportUnknownMemberType]
import itertools
import logging

from biocypher import BioCypher

from open_targets.adapter.context import AcquisitionContext
from open_targets.definition.reference_kg import reference_kg_definition


def main():
    # Initialize BioCypher
    biocypher_instance = BioCypher(
        biocypher_config_path="example/full_graph/biocypher_config.yaml",
    )
    logging.getLogger("biocypher").setLevel(logging.ERROR)
    biocypher_instance.show_ontology_structure()

    context = AcquisitionContext(
        node_definitions=reference_kg_definition.node_definitions,
        edge_definitions=reference_kg_definition.edge_definitions,
        datasets_location="datasets",  # directory containing the downloaded datasets,
    )

    count = 1
    # Stream nodes and edges to BioCypher
    for node_definition in reference_kg_definition.node_definitions:
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
    for edge_definition in reference_kg_definition.edge_definitions:
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

    biocypher_instance.write_import_call()
    biocypher_instance.summary()


if __name__ == "__main__":
    main()
