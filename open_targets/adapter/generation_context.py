from abc import ABC, abstractmethod
from collections.abc import Iterable

from open_targets.adapter.data_wrapper import DataWrapper
from open_targets.adapter.scan_operation import ScanOperation
from open_targets.data.schema_base import Dataset, Field


class GenerationContext(ABC):
    @property
    @abstractmethod
    def datasets(self) -> frozenset[type[Dataset]]:
        """Datasets that are available in the context."""

    @abstractmethod
    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        required_fields: Iterable[type[Field]],
    ) -> Iterable[DataWrapper]:
        """Get a data stream from the dataset using the scan operation."""
