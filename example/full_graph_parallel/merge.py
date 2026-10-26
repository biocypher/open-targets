"""Merge parallel component outputs into one BioCypher-like output directory."""

from __future__ import annotations

import re
import shutil
import sys
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

_IMPORT_ARG_PATTERN = re.compile(r'--(nodes|relationships)="([^"]+)"')


def _import_script_name() -> str:
    """Return the BioCypher import script name for the current platform."""
    if sys.platform.startswith("win"):
        return "neo4j-admin-import-call.ps1"
    return "neo4j-admin-import-call.sh"


def _merge_schema_info(component_dirs: Sequence[Path], destination: Path) -> None:
    """Merge component schema info into one schema file."""
    merged: dict[str, Any] = {}
    for component_dir in component_dirs:
        schema_path = component_dir / "schema_info.yaml"
        if not schema_path.exists():
            continue
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict):
            continue
        for key, value in schema.items():
            if key == "is_schema_info" or not isinstance(value, dict):
                continue
            existing = merged.setdefault(key, value)
            for flag in ("present_in_knowledge_graph", "is_relationship"):
                if value.get(flag):
                    existing[flag] = True

    merged["is_schema_info"] = True
    with destination.open("w", encoding="utf-8") as f:
        yaml.safe_dump(merged, f, sort_keys=True)


def _merge_import_scripts(component_dirs: Sequence[Path], merged_dir: Path) -> None:
    """Build one import script using a component script as the template."""
    node_arguments: list[str] = []
    edge_arguments: list[str] = []
    reference_script: str | None = None
    script_name = _import_script_name()

    for component_dir in component_dirs:
        script_path = component_dir / script_name
        if not script_path.exists():
            continue
        script_text = script_path.read_text(encoding="utf-8")
        if reference_script is None:
            reference_script = script_text

        argument_line = next(
            (line for line in script_text.splitlines() if _IMPORT_ARG_PATTERN.search(line)),
            None,
        )
        if argument_line is None:
            continue

        component_prefix = str(component_dir.resolve())
        merged_prefix = str(merged_dir.resolve())
        for option, path in _IMPORT_ARG_PATTERN.findall(argument_line):
            suffix = path.removeprefix(component_prefix)
            if suffix == path:
                suffix = path.removeprefix(str(component_dir))
            argument = f'--{option}="{merged_prefix}{suffix}"'
            (node_arguments if option == "nodes" else edge_arguments).append(argument)

    if reference_script is None:
        return

    arguments = " ".join([*node_arguments, *edge_arguments])
    merged_lines: list[str] = []
    for original_line in reference_script.splitlines():
        if _IMPORT_ARG_PATTERN.search(original_line):
            base = _IMPORT_ARG_PATTERN.sub("", original_line).rstrip()
            merged_lines.append(f"{base} {arguments}" if arguments else base)
        else:
            merged_lines.append(original_line)

    output_path = merged_dir / script_name
    output_path.write_text("\n".join(merged_lines) + "\n", encoding="utf-8")


def _merge_console_logs(component_dirs: Sequence[Path], merged_dir: Path) -> None:
    """Combine non-empty component console logs into one merged log."""
    with (merged_dir / "console.log").open("w", encoding="utf-8") as output:
        for component_dir in component_dirs:
            log_path = component_dir / "console.log"
            if not log_path.exists():
                continue
            text = log_path.read_text(encoding="utf-8")
            output.write(f"===== {component_dir.name} =====\n")
            output.write(text)
            if not text.endswith("\n"):
                output.write("\n")
            output.write("\n")


def merge_outputs(output_root: Path) -> Path:
    """Merge component outputs and remove the per-component directories."""
    merged_dir = output_root / "merged"
    if merged_dir.exists():
        shutil.rmtree(merged_dir)
    merged_dir.mkdir(parents=True)

    all_component_dirs = [path for path in sorted(output_root.iterdir()) if path.is_dir() and path != merged_dir]
    script_name = _import_script_name()
    component_dirs = [path for path in all_component_dirs if (path / script_name).exists()]
    for component_dir in component_dirs:
        for parquet_file in component_dir.glob("*.parquet"):
            destination = merged_dir / parquet_file.name
            if destination.exists():
                msg = f"Duplicate output file while merging: {parquet_file.name}"
                raise RuntimeError(msg)
            shutil.move(str(parquet_file), str(destination))

    _merge_schema_info(component_dirs, merged_dir / "schema_info.yaml")
    _merge_import_scripts(component_dirs, merged_dir)
    _merge_console_logs(all_component_dirs, merged_dir)

    for component_dir in all_component_dirs:
        shutil.rmtree(component_dir, ignore_errors=True)
    return merged_dir
