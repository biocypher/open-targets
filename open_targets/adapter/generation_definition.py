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


class GenerationDefinition(Generic[TGraphComponent], ABC):
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
    @abstractmethod
    def get_scan_operation(self) -> ScanOperation:
        """Scan operation that is used to generate the graph components."""

    @abstractmethod
    def get_required_fields(self) -> Iterable[type[Field]]:
        """Fields that are requested by this definition.

        The overriding value will be used to calculate the datasets required by
        the adapter in the preparation stage. A dataset field must be included
        here for it to be provided.
        """

    @abstractmethod
    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[TGraphComponent]: ...

    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        return {self.get_scan_operation().dataset}

    def generate(self, context: GenerationContextProtocol) -> Iterable[TGraphComponent]:
        scan_result_stream = context.get_scan_result_stream(self.get_scan_operation(), self.get_required_fields())
        return self.generate_from_scanning(context, scan_result_stream)


@dataclass(frozen=True)
class ExpressionGenerationDefinition(
    ScanningGenerationDefinition[TGraphComponent],
    ABC,
):
    """Definition of a set of nodes to be generated."""

    scan_operation: ScanOperation

    @property
    @abstractmethod
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        """All expressions that are included in this definition."""

    def get_scan_operation(self) -> ScanOperation:
        return self.scan_operation

    def get_required_fields(self) -> Iterable[type[Field]]:
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

    def _normalise_curie(self, string: str):
        if ":" in string:
            return normalize_curie(string, sep=":")
        if "_" in string:
            return normalize_curie(string, sep="_")
        if "/" in string:
            return normalize_curie(string, sep="/")
        return ""

    def _extract_curie_scheme(self, string: str):
        if ":" in string:
            return string.split(":")[0]
        if "_" in string:
            return string.split("_")[0]
        return ""

    def _create_value_getter(
        self,
        expression: Expression[Any],
    ) -> Callable[[DataWrapper], Any]:
        return self.recursive_build_expression_function(expression)

    def _create_key_value_getter(
        self,
        expression: tuple[Expression[Any], Expression[Any]],
    ) -> Callable[[DataWrapper], tuple[str, str]]:
        key_getter = self._create_value_getter(expression[0])
        value_getter = self._create_value_getter(expression[1])
        return lambda record: (key_getter(record), value_getter(record))


@dataclass(frozen=True)
class ExpressionNodeGenerationDefinition(ExpressionGenerationDefinition[NodeInfo]):
    scan_operation: ScanOperation
    primary_id: Source
    labels: Sequence[Source]
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def primary_id_expr(self) -> Expression[str]:
        return self._to_expression(self.primary_id)

    @property
    def labels_expr(self) -> Sequence[Expression[str]]:
        return [self._to_expression(label) for label in self.labels]

    @property
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return [
            (self._to_expression(prop[0]), self._to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (self._to_expression(prop.name), self._to_expression(prop))
            for prop in self.properties
        ]

    @property
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        return [
            self.primary_id_expr,
            *self.labels_expr,
            *[i[0] for i in self.properties_expr],
            *[i[1] for i in self.properties_expr],
        ]

    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[NodeInfo]:
        id_getter = self._create_value_getter(self.primary_id_expr)
        label_getters = [self._create_value_getter(label) for label in self.labels_expr]
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr]

        for data in data_stream:
            yield NodeInfo(
                id=id_getter(data),
                labels=[label_getter(data) for label_getter in label_getters],
                properties=[property_getter(data) for property_getter in property_getters],
            )


@dataclass(frozen=True)
class ExpressionEdgeGenerationDefinition(ExpressionGenerationDefinition[EdgeInfo]):
    primary_id: Source
    source: Source
    target: Source
    labels: Sequence[Source]
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def primary_id_expr(self) -> Expression[str]:
        return self._to_expression(self.primary_id)

    @property
    def source_expr(self) -> Expression[str]:
        return self._to_expression(self.source)

    @property
    def target_expr(self) -> Expression[str]:
        return self._to_expression(self.target)

    @property
    def labels_expr(self) -> Sequence[Expression[str]]:
        return [self._to_expression(label) for label in self.labels]

    @property
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return [
            (self._to_expression(prop[0]), self._to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (self._to_expression(prop.name), self._to_expression(prop))
            for prop in self.properties
        ]

    @property
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        return [
            self.primary_id_expr,
            self.source_expr,
            self.target_expr,
            *self.labels_expr,
            *[i[0] for i in self.properties_expr],
            *[i[1] for i in self.properties_expr],
        ]

    def generate_from_scanning(
        self,
        context: GenerationContextProtocol,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[EdgeInfo]:
        id_getter = self._create_value_getter(self.primary_id_expr)
        source_getter = self._create_value_getter(self.source_expr)
        target_getter = self._create_value_getter(self.target_expr)
        label_getters = [self._create_value_getter(label) for label in self.labels_expr]
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr]

        for data in data_stream:
            yield EdgeInfo(
                id=id_getter(data),
                source_id=source_getter(data),
                target_id=target_getter(data),
                labels=[label_getter(data) for label_getter in label_getters],
                properties=[property_getter(data) for property_getter in property_getters],
            )
