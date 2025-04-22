from collections.abc import Iterable, Sequence
from typing import Any

from open_targets.adapter.acquisition_definition import (
    ScanningAcquisitionDefinition,
    TAcqusitionOutput,
    _ExpressionAcquisitionDefinition,
)
from open_targets.adapter.context_protocol import AcquisitionContextProtocol
from open_targets.adapter.data_wrapper import DataView, DataViewValue
from open_targets.adapter.expression import Expression
from open_targets.adapter.scan_operation import ScanOperation
from open_targets.data.schema import Field
from test.fixture.mock.scan_operation import MockScanOperation
from test.fixture.mock.schema import MockDataset


class MockScanningAcquisitionDefinition(ScanningAcquisitionDefinition[TAcqusitionOutput]):
    def _get_scan_operation(self) -> ScanOperation: ...

    def _get_required_fields(self) -> Iterable[type[Field]]: ...

    def _acquire_from_scanning(
        self,
        context: AcquisitionContextProtocol,
        data_stream: Iterable[DataViewValue],
    ) -> Iterable[TAcqusitionOutput]: ...


class MockSingleExpressionAcquisitionDefinition(_ExpressionAcquisitionDefinition[Any]):
    def __init__(self, expression: Expression[Any]) -> None:
        super().__init__(MockScanOperation(MockDataset))
        self._expression = expression

    def _acquire_from_scanning(
        self,
        context: AcquisitionContextProtocol,
        data_stream: Iterable[DataView],
    ) -> Iterable[Any]:
        value_getter = self._create_value_getter(self._expression)
        return (value_getter(data) for data in data_stream)

    @property
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        return [self._expression]
