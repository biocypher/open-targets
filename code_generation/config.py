"""Functions for generating the config.py file."""

from pathlib import Path
from typing import Any

import tomli
from pydantic.alias_generators import to_snake


def create_config_render_context() -> dict[str, Any]:
    """Return a jinja context for the config.py file.

    Read pyproject.toml and convert the tool.open-targets section to a
    dictionary with UPPER_SNAKE_CASE keys.
    """
    with (Path.cwd() / "pyproject.toml").open("rb") as f:
        pyproject = tomli.load(f)

    name_converted = {to_snake(k).upper(): v for k, v in pyproject["tool"]["open-targets"].items()}

    return {
        "config": name_converted,
    }
