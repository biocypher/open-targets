"""Functions for generating the kg.py file."""

from pathlib import Path, PurePosixPath
from typing import Any

from code_generation.base import GenerationDefinitionBase

# Node definitions that should be hidden (commented out) in kg.py
# Maps definition name to the comment/reason for hiding
HIDDEN_KG_NODE_DEFINITIONS: dict[str, str] = {
    "node_so_term": "Unsure usage",
}

# Edge definitions that should be hidden (commented out) in kg.py
# Maps definition name to the comment/reason for hiding
HIDDEN_KG_EDGE_DEFINITIONS: dict[str, str] = {
    "edge_literature_mentions_entity": "Disabled due to unrealistically huge computational burden",
}


def create_kg_render_context() -> dict[str, Any]:
    """Return a jinja context for the kg.py file."""
    node_dir = Path("open_targets/definition/reference_kg/node")
    edge_dir = Path("open_targets/definition/reference_kg/edge")

    # Get all node files
    node_files = sorted(f.stem for f in node_dir.glob("*.py") if f.name != "__init__.py")

    # Get all edge files
    edge_files = sorted(f.stem for f in edge_dir.glob("*.py") if f.name != "__init__.py")

    # Create node list with hidden flag and comment
    node_list = []
    for n in node_files:
        if n in HIDDEN_KG_NODE_DEFINITIONS:
            # Hidden nodes: don't import, but comment in definitions
            node_list.append(
                {
                    "name": n,
                    "hidden": True,
                    "import": False,
                    "comment": HIDDEN_KG_NODE_DEFINITIONS[n],
                },
            )
        else:
            node_list.append({"name": n, "hidden": False, "import": True})

    # Create edge list with hidden flag and comment
    edge_list = []
    for e in edge_files:
        if e in HIDDEN_KG_EDGE_DEFINITIONS:
            # Hidden edges: don't import, but comment in definitions
            edge_list.append(
                {
                    "name": e,
                    "hidden": True,
                    "import": False,
                    "comment": HIDDEN_KG_EDGE_DEFINITIONS[e],
                },
            )
        else:
            edge_list.append({"name": e, "hidden": False, "import": True})

    # Sort by name to ensure consistent output
    node_list.sort(key=lambda x: x["name"])
    edge_list.sort(key=lambda x: x["name"])

    return {
        "nodes": node_list,
        "edges": edge_list,
    }


class GenerationDefinition(GenerationDefinitionBase):
    """Render the open_targets/definition/reference_kg/kg.py template."""

    template_path = PurePosixPath("open_targets/definition/reference_kg/kg.py.jinja")

    def create_context(self) -> dict[str, Any]:
        return create_kg_render_context()
