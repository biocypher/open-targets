"""Entry point for code generation."""

import sys
from pathlib import Path
from subprocess import run

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from code_generation.base import GenerationDefinitionBase

# The order of the modules is important due to the dependencies between them.
GENERATION_DEFINITION_MODULES = [
    "code_generation.config",
    # "code_generation.schema",
    "code_generation.reference_kg_expression",
    "code_generation.reference_kg_node",
    "code_generation.reference_kg_edge",
    "code_generation.reference_kg_kg",
]


def configure_jinja() -> Environment:
    """Configure the jinja environment."""
    return Environment(
        loader=FileSystemLoader(Path.cwd()),
        lstrip_blocks=True,
        trim_blocks=True,
        undefined=StrictUndefined,
        autoescape=select_autoescape(),
    )


def render(generator: GenerationDefinitionBase) -> None:
    """Render a template with the provided generator."""
    env = configure_jinja()
    template_name = str(generator.template_path)
    template = env.get_template(template_name)
    if template.filename is None:
        msg = f"Template {template_name} has no filename"
        raise ValueError(msg)

    template_full_path = Path(template.filename)
    render_full_path = template_full_path.with_name(template_full_path.stem)
    render_full_path.write_text(template.render(generator.create_context()), encoding="utf-8")

    run(["ruff", "format", str(render_full_path)], check=True)
    run(["ruff", "check", "--fix", "--exit-zero", str(render_full_path)], check=True)


def main() -> None:
    """Run code generation for all definitions."""
    for module_name in GENERATION_DEFINITION_MODULES:
        expression = (
            "from code_generation import generate;"
            f"from {module_name} import GenerationDefinition;"
            f"generate.render(GenerationDefinition())"
        )
        run([sys.executable, "-c", expression], check=True)


if __name__ == "__main__":
    main()
