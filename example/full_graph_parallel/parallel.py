"""Example: build the full reference graph in parallel by label.

Node and edge definitions are grouped by label. Each label is a component,
processed by a bounded process pool, and written to its own BioCypher output
directory.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Final

from biocypher import BioCypher

from example.full_graph_parallel.merge import merge_outputs
from open_targets.adapter.context import AcquisitionContext
from open_targets.config import DATA_REPOSITORY_URLS_S3
from open_targets.definition.reference_kg import reference_kg_definition

if TYPE_CHECKING:
    from collections.abc import Sequence

DATASETS_LOCATION: Final[str] = DATA_REPOSITORY_URLS_S3
LIMIT: Final[int | None] = None
CONCURRENCY: Final[int] = 32
MERGE_RESULTS: Final[bool] = True


def _group_indices(definitions: Sequence[object]) -> dict[str, list[int]]:
    """Group definition indices by label."""
    groups: dict[str, list[int]] = {}
    for index, definition in enumerate(definitions):
        label = str(getattr(definition, "label", "unknown"))
        groups.setdefault(label, []).append(index)
    return groups


def _build_components() -> list[tuple[str, str, tuple[int, ...]]]:
    """Build one component per node/edge label."""
    components: list[tuple[str, str, tuple[int, ...]]] = []
    for kind, definitions in (
        ("node", reference_kg_definition.node_definitions),
        ("edge", reference_kg_definition.edge_definitions),
    ):
        for label, indices in _group_indices(definitions).items():
            components.append((kind, label, tuple(indices)))
    return components


COMPONENTS: Final[list[tuple[str, str, tuple[int, ...]]]] = _build_components()


def _write_component(task: tuple[str, str, tuple[int, ...], str]) -> tuple[str, str]:
    """Acquire all definitions for one label and write them to one output."""
    kind, label, definition_indices, output_root = task
    name = f"{kind}_{label}"
    output_directory = Path(output_root) / name
    output_directory.mkdir(parents=True, exist_ok=True)

    biocypher_instance = BioCypher(
        biocypher_config_path="example/full_graph_parallel/biocypher_config.yaml",
        output_directory=str(output_directory),
    )
    logging.getLogger("biocypher").setLevel(logging.ERROR)

    if kind == "node":
        definitions = [reference_kg_definition.node_definitions[index] for index in definition_indices]
        context = AcquisitionContext(
            node_definitions=definitions,
            edge_definitions=[],
            datasets_location=DATASETS_LOCATION,
            limit=LIMIT,
        )
        for definition in definitions:
            biocypher_instance.write_nodes(context.get_acquisition_generator(definition))
    elif kind == "edge":
        edge_definitions = [reference_kg_definition.edge_definitions[index] for index in definition_indices]
        context = AcquisitionContext(
            node_definitions=[],
            edge_definitions=edge_definitions,
            datasets_location=DATASETS_LOCATION,
            limit=LIMIT,
        )
        for definition in edge_definitions:
            biocypher_instance.write_edges(context.get_acquisition_generator(definition))
    else:
        msg = f"Unknown component kind: {kind}"
        raise ValueError(msg)

    biocypher_instance.write_import_call()
    biocypher_instance.write_schema_info()
    return name, str(output_directory)


def _run_task(task: tuple[str, str, tuple[int, ...], str]) -> tuple[str, str, str, str]:
    """Run one component and capture any exception for the error log."""
    try:
        name, output_directory = _write_component(task)
    except Exception:  # noqa: BLE001
        return ("error", f"{task[0]}_{task[1]}", "", traceback.format_exc())
    return ("ok", name, output_directory, "")


def main() -> None:
    """Build every component and record per-component errors."""
    output_root = Path("biocypher-out") / "parallel" / datetime.now(tz=timezone.utc).strftime("%Y%m%d%H%M%S")
    output_root.mkdir(parents=True, exist_ok=True)
    errors_path = Path("parallel_errors.log")
    errors_path.write_text("", encoding="utf-8")
    process_count = min(CONCURRENCY, len(COMPONENTS))

    print(  # noqa: T201
        f"Building {len(COMPONENTS)} components with {process_count} processes into {output_root}",
        flush=True,
    )

    tasks = [(kind, label, indices, str(output_root)) for kind, label, indices in COMPONENTS]
    succeeded = 0
    failed = 0
    mp_context = mp.get_context("spawn")
    with mp_context.Pool(process_count) as pool:
        for status, name, output_directory, detail in pool.imap_unordered(_run_task, tasks, chunksize=1):
            if status == "ok":
                succeeded += 1
                print(f"OK {name} {output_directory}", flush=True)  # noqa: T201
                continue

            failed += 1
            print(f"ERROR {name}", flush=True)  # noqa: T201
            with errors_path.open("a", encoding="utf-8") as f:
                f.write(f"=== {name} ===\n{detail}\n")

    print(  # noqa: T201
        f"Finished: ok={succeeded} error={failed} output={output_root} errors={errors_path}",
        flush=True,
    )
    if MERGE_RESULTS:
        merged_dir = merge_outputs(output_root)
        print(f"Merged output: {merged_dir}", flush=True)  # noqa: T201


if __name__ == "__main__":
    main()
