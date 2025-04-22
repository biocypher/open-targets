import uuid
from typing import Any
from unittest.mock import MagicMock

import pytest

from open_targets.adapter.acquisition_definition import (
    ExpressionEdgeAcquisitionDefinition,
    ExpressionNodeAcquisitionDefinition,
)
from open_targets.adapter.data_wrapper import DataView
from open_targets.adapter.expression import (
    BuildCurieExpression,
    DataSourceToLicenceExpression,
    Expression,
    ExtractCuriePrefixExpression,
    ExtractSubstringExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
    StringLowerExpression,
    ToStringExpression,
    TransformExpression,
)
from open_targets.adapter.licence import License
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation, RowScanOperation, ScanOperation
from open_targets.data.schema_base import SequenceField
from test.fixture.fake.schema import DatasetFake
from test.fixture.mock.acquisition_definition import (
    MockScanningAcquisitionDefinition,
    MockSingleExpressionAcquisitionDefinition,
)
from test.fixture.mock.context import MockAcquisitionContext
from test.fixture.mock.scan_operation import MockScanOperation
from test.fixture.mock.schema import MockDataset, MockField, mock_field_factory


class TestScanningAcquisitionDefinition:
    @pytest.mark.parametrize(
        "scan_operation",
        [
            RowScanOperation(DatasetFake),
            ExplodingScanOperation(DatasetFake, SequenceField),
        ],
    )
    def test_get_required_datasets(self, scan_operation: ScanOperation) -> None:
        definition = MockScanningAcquisitionDefinition[Any]()
        definition._get_scan_operation = MagicMock(return_value=scan_operation)
        assert list(definition.get_required_datasets()) == [scan_operation.dataset]

    def test_acquire(self) -> None:
        context = MockAcquisitionContext()
        definition = MockScanningAcquisitionDefinition[Any]()
        stream = [uuid.uuid4() for _ in range(10)]
        context.get_scan_result_stream = MagicMock(return_value=stream)
        definition._acquire_from_scanning = MagicMock(return_value=stream)
        assert list(definition.acquire(context)) == stream
        definition._acquire_from_scanning.assert_called_once_with(context, stream)


class TestExpressionAcquisitionDefinition:
    def perform_test(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        def test():
            context = MockAcquisitionContext()
            context.get_scan_result_stream = MagicMock(return_value=[field_map])
            definition = MockSingleExpressionAcquisitionDefinition(expression)
            result = next(iter(definition.acquire(context)))
            assert result == expected

        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                test()
        else:
            test()

    def test_field_expression(self) -> None:
        self.perform_test({MockField: 1}, FieldExpression(MockField), 1)

    def test_literal_expression(self) -> None:
        self.perform_test({MockField: 1}, LiteralExpression(1), 1)

    @pytest.mark.parametrize(
        ("field_map", "expression", "expected"),
        [
            ({MockField: "test"}, TransformExpression(FieldExpression(MockField), str.upper), "TEST"),
            ({}, TransformExpression(None, lambda _: "TEST"), "TEST"),
        ],
    )
    def test_transform_expression(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        self.perform_test(field_map, expression, expected)

    def test_to_string_expression(self) -> None:
        self.perform_test({MockField: 1}, ToStringExpression(FieldExpression(MockField)), "1")

    def test_string_concatenation_expression(self) -> None:
        self.perform_test(
            {MockField: 1},
            StringConcatenationExpression(
                [ToStringExpression(FieldExpression(MockField)), LiteralExpression("test")],
            ),
            "1test",
        )

    def test_string_lower_expression(self) -> None:
        self.perform_test(
            {MockField: "FIELD"},
            StringLowerExpression(ToStringExpression(FieldExpression(MockField))),
            "field",
        )

    @pytest.mark.parametrize(
        ("field_map", "expression", "expected"),
        [
            (
                {MockField: "gO"},
                BuildCurieExpression(FieldExpression(MockField), LiteralExpression("AbCdEf")),
                "go:AbCdEf",
            ),
            (
                {MockField: "gO"},
                BuildCurieExpression(FieldExpression(MockField), LiteralExpression("AbCdEf"), normalise=False),
                "gO:AbCdEf",
            ),
        ],
    )
    def test_build_curie_expression(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        self.perform_test(field_map, expression, expected)

    @pytest.mark.parametrize(
        ("field_map", "expression", "expected"),
        [
            (
                {MockField: "gO:AbCdEf"},
                ExtractCuriePrefixExpression(ToStringExpression(FieldExpression(MockField))),
                "go",
            ),
            (
                {MockField: "gO:AbCdEf"},
                ExtractCuriePrefixExpression(ToStringExpression(FieldExpression(MockField)), normalise=False),
                "gO",
            ),
        ],
    )
    def test_extract_curie_prefix_expression(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        self.perform_test(field_map, expression, expected)

    def test_normalise_curie_expression(self) -> None:
        self.perform_test(
            {MockField: "gO_AbCdEf"},
            NormaliseCurieExpression(ToStringExpression(FieldExpression(MockField))),
            "go:AbCdEf",
        )

    @pytest.mark.parametrize(
        ("field_map", "expression", "expected"),
        [
            (
                {MockField: "gO_AbCdEf"},
                ExtractSubstringExpression(
                    ToStringExpression(FieldExpression(MockField)),
                    LiteralExpression("_"),
                    0,
                ),
                "gO",
            ),
            (
                {MockField: "gO_AbCdEf"},
                ExtractSubstringExpression(
                    ToStringExpression(FieldExpression(MockField)),
                    LiteralExpression("_"),
                    1,
                ),
                "AbCdEf",
            ),
            (
                {MockField: "gO_AbCdEf"},
                ExtractSubstringExpression(
                    ToStringExpression(FieldExpression(MockField)),
                    LiteralExpression(":"),
                    0,
                ),
                "gO_AbCdEf",
            ),
        ],
    )
    def test_extract_substring_expression(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        self.perform_test(field_map, expression, expected)

    @pytest.mark.parametrize(
        ("field_map", "expression", "expected"),
        [
            (
                {MockField: "test"},
                DataSourceToLicenceExpression(ToStringExpression(FieldExpression(MockField))),
                str(License.UNKNOWN),
            ),
            (
                {MockField: "chembl"},
                DataSourceToLicenceExpression(ToStringExpression(FieldExpression(MockField))),
                str(License.CC_BY_SA_3_0),
            ),
        ],
    )
    def test_data_source_to_licence_expression(
        self,
        field_map: DataView,
        expression: Expression[Any],
        expected: Any,
    ) -> None:
        self.perform_test(field_map, expression, expected)


_mock_field_a = mock_field_factory("mock_field_a")
_mock_field_b = mock_field_factory("mock_field_b")
_mock_field_c = mock_field_factory("mock_field_c")
_mock_field_d = mock_field_factory("mock_field_d")
_mock_field_e = mock_field_factory("mock_field_e")


class TestExpressionNodeAcquisitionDefinition:
    @pytest.mark.parametrize(
        ("field_map", "primary_id", "label", "properties", "expected"),
        [
            (
                {},
                "id",
                "label",
                [("property_a", "property_a_value")],
                NodeInfo(
                    id="id",
                    label="label",
                    properties={
                        "property_a": "property_a_value",
                    },
                ),
            ),
            (
                {
                    _mock_field_a: "id",
                    _mock_field_b: "label",
                    _mock_field_c: "mock_field_c_value",
                },
                _mock_field_a,
                _mock_field_b,
                [_mock_field_c],
                NodeInfo(
                    id="id",
                    label="label",
                    properties={
                        "mock_field_c": "mock_field_c_value",
                    },
                ),
            ),
            (
                {},
                LiteralExpression("id"),
                LiteralExpression("label"),
                [(LiteralExpression("property_a"), LiteralExpression("property_a_value"))],
                NodeInfo(
                    id="id",
                    label="label",
                    properties={
                        "property_a": "property_a_value",
                    },
                ),
            ),
        ],
    )
    def test_node_acquisition_definition(
        self,
        field_map: DataView,
        primary_id: str,
        label: str,
        properties: list[Any],
        expected: Any,
    ) -> None:
        definition = ExpressionNodeAcquisitionDefinition(
            MockScanOperation(MockDataset),
            primary_id,
            label,
            properties,
        )
        context = MockAcquisitionContext()
        context.get_scan_result_stream = MagicMock(return_value=[field_map])
        result = next(iter(definition.acquire(context)))
        assert result == expected


class TestExpressionEdgeAcquisitionDefinition:
    @pytest.mark.parametrize(
        ("field_map", "primary_id", "source", "target", "label", "properties", "expected"),
        [
            (
                {},
                "id",
                "source",
                "target",
                "label",
                [("property_a", "property_a_value")],
                EdgeInfo(
                    id="id",
                    source_id="source",
                    target_id="target",
                    label="label",
                    properties={
                        "property_a": "property_a_value",
                    },
                ),
            ),
            (
                {
                    _mock_field_a: "id",
                    _mock_field_b: "source",
                    _mock_field_c: "target",
                    _mock_field_d: "label",
                    _mock_field_e: "mock_field_e_value",
                },
                _mock_field_a,
                _mock_field_b,
                _mock_field_c,
                _mock_field_d,
                [_mock_field_e],
                EdgeInfo(
                    id="id",
                    source_id="source",
                    target_id="target",
                    label="label",
                    properties={
                        "mock_field_e": "mock_field_e_value",
                    },
                ),
            ),
            (
                {},
                LiteralExpression("id"),
                LiteralExpression("source"),
                LiteralExpression("target"),
                LiteralExpression("label"),
                [(LiteralExpression("property_a"), LiteralExpression("property_a_value"))],
                EdgeInfo(
                    id="id",
                    source_id="source",
                    target_id="target",
                    label="label",
                    properties={
                        "property_a": "property_a_value",
                    },
                ),
            ),
        ],
    )
    def test_edge_acquisition_definition(
        self,
        field_map: DataView,
        primary_id: str,
        source: str,
        target: str,
        label: str,
        properties: list[Any],
        expected: Any,
    ) -> None:
        definition = ExpressionEdgeAcquisitionDefinition(
            MockScanOperation(MockDataset),
            primary_id,
            source,
            target,
            label,
            properties,
        )
        context = MockAcquisitionContext()
        context.get_scan_result_stream = MagicMock(return_value=[field_map])
        result = next(iter(definition.acquire(context)))
        assert result == expected
