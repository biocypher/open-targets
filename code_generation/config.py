"""Functions for generating the config.py file.

All project related settings are written in `pyproject.toml` for the sake of
single source of truth. For these settings to be accessible in Python runtime,
jinja is used to read the file and generate constants in `config.py`.
"""

from collections.abc import Iterator, Mapping
from pathlib import Path, PurePosixPath
from typing import Any, cast

import tomli

from code_generation.base import GenerationDefinitionBase


def flatten_config(
    config: Mapping[str, object],
    prefix: str = "",
) -> Iterator[tuple[str, str]]:
    """Yield flattened constant names and string values."""
    for key, value in config.items():
        name = f"{prefix}{key.replace('-', '_')}".upper()
        if isinstance(value, Mapping):
            yield from flatten_config(cast("Mapping[str, object]", value), f"{name}_")
        else:
            yield name, cast("str", value)


def create_config_render_context() -> dict[str, Any]:
    """Return a jinja context for the config.py file.

    Read pyproject.toml and convert the tool.open-targets section to flattened
    constants with UPPER_SNAKE_CASE keys.
    """
    with (Path.cwd() / "pyproject.toml").open("rb") as f:
        config = tomli.load(f)["tool"]["open-targets"]
    return {"config": [(name, repr(value)) for name, value in flatten_config(config)]}


class GenerationDefinition(GenerationDefinitionBase):
    """Render the open_targets/config.py template."""

    template_path = PurePosixPath("open_targets/config.py.jinja")

    def create_context(self) -> dict[str, Any]:
        return create_config_render_context()
