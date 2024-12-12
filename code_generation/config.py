from pathlib import Path
from typing import Any

import tomli


def create_config_render_context() -> dict[str, Any]:
    with (Path.cwd() / "pyproject.toml").open("rb") as f:
        pyproject = tomli.load(f)

    return {
        "data_version": pyproject["tool"]["open-targets"]["data-version"],
    }
