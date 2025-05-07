from collections.abc import Iterable, Sequence
from pathlib import Path

from open_targets.adapter.context_protocol import AcquisitionContextProtocol
from open_targets.adapter.data_view import DataView
from open_targets.adapter.scan_operation import ScanOperation
from open_targets.data.schema_base import Dataset, Field


class MockAcquisitionContext(AcquisitionContextProtocol):
    def get_dataset_path(self, dataset: type[Dataset]) -> Path: ...

    def get_scan_result_stream(
        self,
        scan_operation: ScanOperation,
        requested_fields: Sequence[type[Field]],
    ) -> Iterable[DataView]: ...
