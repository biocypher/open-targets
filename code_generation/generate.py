from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from code_generation.config import create_config_render_context
from code_generation.schema import create_schema_render_context


def configure_jinja() -> Environment:
    return Environment(
        loader=FileSystemLoader(Path.cwd()),
        lstrip_blocks=True,
        trim_blocks=True,
        undefined=StrictUndefined,  # raise an error if a variable is not defined rather silently providing empty string
        autoescape=select_autoescape(),
    )


def render(env: Environment, template_local_path: PurePosixPath, context_creator: Callable[[], dict[str, Any]]) -> None:
    template_name = str(template_local_path)
    template = env.get_template(template_name)
    if template.filename is None:
        msg = f"Template {template_name} has no filename"
        raise ValueError(msg)

    template_full_path = Path(template.filename)
    render_full_path = template_full_path.with_name(template_full_path.stem)
    context = context_creator()
    render_full_path.write_text(template.render(context))


env = configure_jinja()

# Order matters here due to dependencies, for example, schema.py depends on
# generated config.py.
render(env, PurePosixPath("open_targets/config.py.jinja"), create_config_render_context)
render(env, PurePosixPath("open_targets/data/schema.py.jinja"), create_schema_render_context)
