from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass
class NodeInfo:
    id: str
    label: str
    properties: Mapping[str, str]

    def __iter__(self) -> Iterator[Any]:
        return iter((self.id, self.label, self.properties))

    def __len__(self) -> int:
        return 3

    def as_tuple(self) -> tuple[str, str, Mapping[str, str]]:
        return self.id, self.label, self.properties


@dataclass
class EdgeInfo:
    id: str
    source_id: str
    target_id: str
    label: str
    properties: Mapping[str, str]

    def __iter__(self) -> Iterator[Any]:
        return iter((self.id, self.source_id, self.target_id, self.label, self.properties))

    def __len__(self) -> int:
        return 5

    def as_tuple(self) -> tuple[str, str, str, str, Mapping[str, str]]:
        return self.id, self.source_id, self.target_id, self.label, self.properties
