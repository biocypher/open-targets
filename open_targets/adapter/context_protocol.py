from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from open_targets.adapter.data_wrapper import DataWrapper
from open_targets.adapter.scan_operation import ScanOperation
from open_targets.data.schema_base import Dataset, Field


class GenerationContextProtocol(Protocol):
    def get_dataset_path(self, dataset: type[Dataset]) -> Path: ...

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]: ...
