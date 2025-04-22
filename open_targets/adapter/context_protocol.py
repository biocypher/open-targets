"""Definition of the generation context protocol."""

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from open_targets.adapter.data_view import DataView
from open_targets.adapter.scan_operation import ScanOperation
from open_targets.data.schema_base import Dataset, Field


class AcquisitionContextProtocol(Protocol):
    """Protocol for the generation context.

    A generation context provides information of a generation session and low
    level access to datasets. This protocol is an abstract layer over the query
    engine.
    """

    def get_dataset_path(self, dataset: type[Dataset]) -> Path:
        """Get the path to the dataset."""
        ...

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        requested_fields: Iterable[type[Field]],
    ) -> Iterable[DataView]:
        """Get the scan result stream.

        Each item yielded by the stream is a data view to allow access by field
        classes. The values produced depend on the scan operation and the
        required fields provided. For details of scan operations, see their
        docstrings. The actual query executed could be optimised but not
        guaranteed.
        """
        ...
