"""Definition of generation definitions.

Generation definitions also define the actual logic querying the datasets.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeAlias, TypeVar

from bioregistry.resolve import normalize_curie, normalize_parsed_curie, normalize_prefix

from open_targets.adapter.context_protocol import GenerationContextProtocol
from open_targets.adapter.data_wrapper import DataWrapper
from open_targets.adapter.expression import (
    BuildCurieExpression,
    DataSourceToLicenceExpression,
    Expression,
    ExtractCurieSchemeExpression,
    ExtractSubstringExpression,
    FieldExpression,
    LiteralExpression,
    NormaliseCurieExpression,
    StringConcatenationExpression,
    StringLowerExpression,
    ToStringExpression,
    TransformExpression,
    recursive_get_dependent_fields,
)
from open_targets.adapter.licence import get_datasource_license
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import FlattenedScanOperation, ScanOperation
from open_targets.data.schema import Field
from open_targets.data.schema_base import Dataset

TGraphComponent = TypeVar("TGraphComponent", NodeInfo, EdgeInfo)

Source: TypeAlias = str | type[Field] | Expression[Any]

CURIE_SEPARATORS = [":", "_", "/"]


class GenerationDefinition(Generic[TGraphComponent], ABC):
    """Base class for all generation definitions.

    A generation definition describes how to generate a set of nodes/edges. High
    level definitions are provided but in the case of more complex generation
    logic, a subclass of this class can be used to query the dataset directly to
    provide the specific logic.
    """

    @abstractmethod
    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""

    @abstractmethod
    def generate(self, context: GenerationContextProtocol) -> Iterable[TGraphComponent]:
        """Generate graph components by directly accessing the context."""


class ScanningGenerationDefinition(
    GenerationDefinition[TGraphComponent],
    ABC,
):
    """Generation definition that uses a scan operation to generate.

    The dataset query is abstracted out by the scan operation which determines
    the fashion of data query. Items yielded are also wrapped for easy access
    to the data fields.
    """

    @abstractmethod
    def get_scan_operation(self) -> ScanOperation:
        """Scan operation that is used to generate the graph components."""

    @abstractmethod
    def get_required_fields(self) -> Iterable[type[Field]]:
        """Fields that are requested by this definition."""

    @abstractmethod
    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[TGraphComponent]:
        """Generate graph components from the scanning result stream."""

    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""
        return {self.get_scan_operation().dataset}

    def generate(self, context: GenerationContextProtocol) -> Iterable[TGraphComponent]:
        """Create the scanning result stream from the low level access."""
        scan_result_stream = context.get_scan_result_stream(self.get_scan_operation(), self.get_required_fields())
        return self.generate_from_scanning(context, scan_result_stream)


@dataclass(frozen=True)
class ExpressionGenerationDefinition(
    ScanningGenerationDefinition[TGraphComponent],
    ABC,
):
    """Generation definition that is described by expressions.

    Expressions are used to describe how to obtain values of the attributes of
    nodes or edges from a scanning result.
    """

    scan_operation: ScanOperation

    @property
    @abstractmethod
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        """All expressions that are included in this definition."""

    def get_scan_operation(self) -> ScanOperation:
        """Return the provided scan operation."""
        return self.scan_operation

    def get_required_fields(self) -> Iterable[type[Field]]:
        """Get all fields that are required by all the expressions."""
        fields = set[type[Field]]()
        for expression in self._all_expressions:
            fields.update(recursive_get_dependent_fields(expression))
        if isinstance(self.scan_operation, FlattenedScanOperation):
            fields.add(self.scan_operation.flattened_field)
        return fields

    def _to_expression(self, value: str | type[Field] | Expression[Any]) -> Expression[Any]:
        if isinstance(value, str):
            return LiteralExpression(value)
        if isinstance(value, type):
            return FieldExpression(value)
        return value

    def recursive_build_expression_function(self, expression: Expression[Any]) -> Callable[[DataWrapper], Any]:
        """Build a function chain that evaluates the expression."""
        match expression:
            case FieldExpression():
                return lambda data: data[expression.field]
            case LiteralExpression():
                return lambda _: expression.value
            case TransformExpression():
                return lambda data: expression.function(data)
            case ToStringExpression():
                func = self.recursive_build_expression_function(expression.expression)
                return lambda data: str(func(data))
            case StringConcatenationExpression():
                funcs = [self.recursive_build_expression_function(e) for e in expression.expressions]
                return lambda data: "".join(func(data) for func in funcs)
            case StringLowerExpression():
                func = self.recursive_build_expression_function(expression.expression)
                return lambda data: func(data).lower()
            case BuildCurieExpression():
                return self._get_curie_builder(expression)
            case ExtractCurieSchemeExpression():
                func = self.recursive_build_expression_function(expression.expression)
                return (
                    (lambda data: normalize_prefix(self._extract_curie_scheme(func(data))))
                    if expression.normalise
                    else (lambda data: self._extract_curie_scheme(func(data)))
                )
            case NormaliseCurieExpression():
                func = self.recursive_build_expression_function(expression.expression)
                return lambda data: self._normalise_curie(func(data))
            case ExtractSubstringExpression():
                func = self.recursive_build_expression_function(expression.expression)
                separator_func = self.recursive_build_expression_function(expression.separator)
                return lambda data: func(data).split(separator_func(data))[expression.index]
            case DataSourceToLicenceExpression():
                func = self.recursive_build_expression_function(expression.datasource)
                return lambda data: get_datasource_license(func(data))
            case _:
                msg = f"Unsupported expression: {expression}"
                raise ValueError(msg)

    def _get_curie_builder(self, expression: BuildCurieExpression) -> Callable[[DataWrapper], str]:
        scheme_func = self.recursive_build_expression_function(expression.scheme)
        path_func = self.recursive_build_expression_function(expression.path)

        def normalise_curie_builder(data: DataWrapper) -> str:
            scheme, path = normalize_parsed_curie(scheme_func(data), path_func(data))
            scheme = "" if scheme is None else scheme
            path = "" if path is None else path
            return f"{scheme}:{path}"

        return (
            normalise_curie_builder
            if expression.normalised
            else (lambda data: f"{scheme_func(data)}:{path_func(data)}")
        )

    def _normalise_curie(self, string: str) -> str:
        for sep in CURIE_SEPARATORS:
            if sep in string:
                result = normalize_curie(string, sep=sep)
                if result is not None:
                    return result
                msg = f"Failed to normalize curie: {string} with separator: {sep}"
                raise ValueError(msg)
        msg = f"Failed to normalize curie: {string}"
        raise ValueError(msg)

    def _extract_curie_scheme(self, string: str) -> str:
        for sep in CURIE_SEPARATORS:
            if sep in string:
                return string.split(sep)[0]
        msg = f"Failed to extract curie scheme from: {string}"
        raise ValueError(msg)

    def _create_value_getter(
        self,
        expression: Expression[Any],
    ) -> Callable[[DataWrapper], Any]:
        func = self.recursive_build_expression_function(expression)
        return lambda data: str(func(data))


@dataclass(frozen=True)
class ExpressionNodeGenerationDefinition(ExpressionGenerationDefinition[NodeInfo]):
    """Expression generation definition for nodes."""

    scan_operation: ScanOperation
    primary_id: Source
    label: Source
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def _primary_id_expr(self) -> Expression[str]:
        return self._to_expression(self.primary_id)

    @property
    def _label_expr(self) -> Expression[str]:
        return self._to_expression(self.label)

    @property
    def _property_exprs(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return [
            (self._to_expression(prop[0]), self._to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (self._to_expression(prop.name), self._to_expression(prop))
            for prop in self.properties
        ]

    @property
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        return [
            self._primary_id_expr,
            self._label_expr,
            *[i[0] for i in self._property_exprs],
            *[i[1] for i in self._property_exprs],
        ]

    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[NodeInfo]:
        """Build the functions that compute the values from the data stream."""
        id_getter = self._create_value_getter(self._primary_id_expr)
        label_getter = self._create_value_getter(self._label_expr)
        property_getters = [
            (self._create_value_getter(key_expr), self._create_value_getter(value_expr))
            for key_expr, value_expr in self._property_exprs
        ]

        for data in data_stream:
            try:
                yield NodeInfo(
                    id=id_getter(data),
                    label=label_getter(data),
                    properties={key_getter(data): value_getter(data) for key_getter, value_getter in property_getters},
                )
            except Exception:  # noqa: PERF203
                logging.exception("Failed to generate node from data: %s", data)


@dataclass(frozen=True)
class ExpressionEdgeGenerationDefinition(ExpressionGenerationDefinition[EdgeInfo]):
    """Expression generation definition for edges."""

    primary_id: Source
    source: Source
    target: Source
    label: Source
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def _primary_id_expr(self) -> Expression[str]:
        return self._to_expression(self.primary_id)

    @property
    def _source_expr(self) -> Expression[str]:
        return self._to_expression(self.source)

    @property
    def _target_expr(self) -> Expression[str]:
        return self._to_expression(self.target)

    @property
    def _label_expr(self) -> Expression[str]:
        return self._to_expression(self.label)

    @property
    def _property_exprs(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return [
            (self._to_expression(prop[0]), self._to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (self._to_expression(prop.name), self._to_expression(prop))
            for prop in self.properties
        ]

    @property
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        return [
            self._primary_id_expr,
            self._source_expr,
            self._target_expr,
            self._label_expr,
            *[i[0] for i in self._property_exprs],
            *[i[1] for i in self._property_exprs],
        ]

    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[EdgeInfo]:
        """Build the functions that compute the values from the data stream."""
        id_getter = self._create_value_getter(self._primary_id_expr)
        source_getter = self._create_value_getter(self._source_expr)
        target_getter = self._create_value_getter(self._target_expr)
        label_getter = self._create_value_getter(self._label_expr)
        property_getters = [
            (self._create_value_getter(key_expr), self._create_value_getter(value_expr))
            for key_expr, value_expr in self._property_exprs
        ]

        for data in data_stream:
            try:
                yield EdgeInfo(
                    id=id_getter(data),
                    source_id=source_getter(data),
                    target_id=target_getter(data),
                    label=label_getter(data),
                    properties={key_getter(data): value_getter(data) for key_getter, value_getter in property_getters},
                )
            except Exception:  # noqa: PERF203
                logging.exception("Failed to generate edge from data: %s", data)
