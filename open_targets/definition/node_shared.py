"""Definition of shared properties for nodes."""

from collections.abc import Sequence
from typing import Final

from open_targets.config import DATA_VERSION

node_static_properties: Final[Sequence[tuple[str, str]]] = [
    ("version", DATA_VERSION),
    ("source", "Open Targets"),
    ("licence", "https://platform-docs.opentargets.org/licence"),
]
