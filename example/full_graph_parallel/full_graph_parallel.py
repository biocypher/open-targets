"""Example: build the full reference graph in parallel by label.

Node and edge definitions are grouped by label. Each label is a component,
processed by a bounded process pool, and written to its own BioCypher output
directory. Component console output is saved in its output directory and merged
into the final output when merging is enabled.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Final, cast

from example.full_graph_parallel.console import capture_output, run_with_progress
from example.full_graph_parallel.merge import merge_outputs
from open_targets.adapter.context import AcquisitionContext
from open_targets.config import DATA_REPOSITORY_URLS_S3
from open_targets.definition.reference_kg import reference_kg_definition

if TYPE_CHECKING:
    from multiprocessing.queues import Queue as MPQueue

DATASETS_LOCATION: Final[str] = DATA_REPOSITORY_URLS_S3
LIMIT: Final[int | None] = None
CONCURRENCY: Final[int] = 32
MERGE_RESULTS: Final[bool] = True


def _build_components() -> list[tuple[str, str, tuple[int, ...]]]:
    """Build one component per node/edge label."""
    components: list[tuple[str, str, tuple[int, ...]]] = []
    for kind, definitions in (
        ("node", reference_kg_definition.node_definitions),
        ("edge", reference_kg_definition.edge_definitions),
    ):
        groups: dict[str, list[int]] = {}
        for index, definition in enumerate(definitions):
            label = str(getattr(definition, "label", "unknown"))
            groups.setdefault(label, []).append(index)
        components.extend((kind, label, tuple(indices)) for label, indices in groups.items())
    return components


COMPONENTS: Final[list[tuple[str, str, tuple[int, ...]]]] = _build_components()


def _build_component(
    kind: str,
    definition_indices: tuple[int, ...],
    output_directory: Path,
) -> None:
    """Build one label component into an already created output directory."""
    logger = logging.getLogger("biocypher")
    logger.setLevel(logging.INFO)
    from biocypher import BioCypher  # noqa: PLC0415

    biocypher_instance = BioCypher(
        biocypher_config_path="example/full_graph_parallel/biocypher_config.yaml",
        output_directory=str(output_directory),
    )
    logger.setLevel(logging.ERROR)

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


def _task_name(task: tuple[str, str, tuple[int, ...], str]) -> str:
    """Return the display name of a component task."""
    return f"{task[0]}_{task[1]}"


def _write_component(task: tuple[str, str, tuple[int, ...], str], event_queue: MPQueue) -> None:
    """Acquire all definitions for one label and write them to one output."""
    kind, _label, definition_indices, output_root = task
    name = _task_name(task)
    output_directory = Path(output_root) / name
    output_directory.mkdir(parents=True, exist_ok=True)
    log_path = output_directory / "console.log"

    try:
        with capture_output(log_path, name, event_queue):
            _build_component(kind, definition_indices, output_directory)
    except Exception:
        with log_path.open("a", encoding="utf-8") as log_file:
            traceback.print_exc(file=log_file)
        raise


def _run_task(task: tuple[str, str, tuple[int, ...], str], event_queue: MPQueue) -> None:
    """Run one component and report its final status to the parent."""
    name = _task_name(task)
    try:
        _write_component(task, event_queue)
    except Exception:  # noqa: BLE001
        event_queue.put(("done", name, "error", traceback.format_exc()))
    else:
        event_queue.put(("done", name, "ok", ""))


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
    mp_context = mp.get_context("spawn")
    manager = mp_context.Manager()
    event_queue = cast("MPQueue", manager.Queue())
    try:
        with mp_context.Pool(process_count) as pool:
            succeeded, failed = run_with_progress(
                pool,
                tasks,
                process_count,
                errors_path,
                event_queue,
                _run_task,
                _task_name,
            )
    finally:
        manager.shutdown()

    print(  # noqa: T201
        f"Finished: {succeeded}/{len(tasks)} labels completed, {failed} failed.",
        flush=True,
    )
    print(f"Output: {output_root}", flush=True)  # noqa: T201
    print(f"Errors: {errors_path}", flush=True)  # noqa: T201
    if MERGE_RESULTS:
        merged_dir = merge_outputs(output_root)
        print(f"Merged output: {merged_dir}", flush=True)  # noqa: T201


if __name__ == "__main__":
    main()
