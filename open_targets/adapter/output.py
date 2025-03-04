from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class NodeInfo:
    id: str
    labels: Sequence[str]
    properties: Sequence[tuple[str, str]]

    def as_tuple(self) -> tuple[str, Sequence[str], Sequence[tuple[str, str]]]:
        return self.id, self.labels, self.properties


@dataclass
class EdgeInfo:
    id: str
    source_id: str
    target_id: str
    labels: Sequence[str]
    properties: Sequence[tuple[str, str]]

    def as_tuple(self) -> tuple[str, str, str, Sequence[str], Sequence[tuple[str, str]]]:
        return self.id, self.source_id, self.target_id, self.labels, self.properties
