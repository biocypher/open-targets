from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeAlias, TypeVar

from open_targets.adapter.data_wrapper import DataWrapper
from open_targets.adapter.expression import (
    Expression,
    FieldExpression,
    LiteralExpression,
    StringConcatenationExpression,
    ToStringExpression,
    TransformExpression,
    recursive_get_dependent_fields,
)
from open_targets.adapter.generation_context import GenerationContext
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import RowScanOperation, ScanOperation
from open_targets.data.schema import Field
from open_targets.data.schema_base import Dataset

TGraphComponent = TypeVar("TGraphComponent", NodeInfo, EdgeInfo)

Source: TypeAlias = str | type[Field] | Expression[Any]


class GenerationDefinition(Generic[TGraphComponent], ABC):
    @abstractmethod
    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""

    @abstractmethod
    def generate(self, context: GenerationContext) -> Iterable[TGraphComponent]:
        """Generate graph components by directly accessing the context."""


class ScanningGenerationDefinition(
    GenerationDefinition[TGraphComponent],
    ABC,
):
    @property
    @abstractmethod
    def scan_operation(self) -> ScanOperation:
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
        context: GenerationContext,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[TGraphComponent]: ...

    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        return {self.scan_operation.dataset}

    def generate(self, context: GenerationContext) -> Iterable[TGraphComponent]:
        scan_result_stream = context.get_scan_result_stream(self.scan_operation, self.get_required_fields())
        return self.generate_from_scanning(context, scan_result_stream)


class ExpressionGenerationDefinition(
    ScanningGenerationDefinition[TGraphComponent],
    ABC,
):
    """Definition of a set of nodes to be generated."""

    @property
    @abstractmethod
    def _all_expressions(self) -> set[Expression[Any]]:
        """All expressions that are included in this definition."""

    @property
    def scan_operation(self) -> ScanOperation:
        return RowScanOperation(dataset=next(iter(self.get_required_fields())).dataset)

    def get_required_fields(self) -> Iterable[type[Field]]:
        fields = set[type[Field]]()
        for expression in self._all_expressions:
            fields.update(recursive_get_dependent_fields(expression))
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
                return lambda record: record[expression.field]
            case LiteralExpression():
                return lambda _: expression.value
            case TransformExpression():
                return lambda record: expression.function(record)
            case ToStringExpression():
                return lambda record: str(self.recursive_build_expression_function(expression.expression)(record))
            case StringConcatenationExpression():
                return lambda record: "".join(
                    self.recursive_build_expression_function(expression)(record)
                    for expression in expression.expressions
                )
            case _:
                return lambda _: expression

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
    def _all_expressions(self) -> set[Expression[Any]]:
        return {
            self.primary_id_expr,
            *self.labels_expr,
            *[i[0] for i in self.properties_expr],
            *[i[1] for i in self.properties_expr],
        }

    def generate_from_scanning(
        self,
        context: GenerationContext,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[NodeInfo]:
        id_getter = self._create_value_getter(self.primary_id_expr)
        label_getters = [self._create_value_getter(label) for label in self.labels_expr]
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr] + [
            self._create_key_value_getter((LiteralExpression(prop[0]), LiteralExpression(prop[1])))
            for prop in context.static_properties
        ]

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
    def _all_expressions(self) -> set[Expression[Any]]:
        return {
            self.primary_id_expr,
            self.source_expr,
            self.target_expr,
            *self.labels_expr,
            *[i[0] for i in self.properties_expr],
            *[i[1] for i in self.properties_expr],
        }

    def generate_from_scanning(
        self,
        context: GenerationContext,
        data_stream: Iterable[DataWrapper],
    ) -> Iterable[EdgeInfo]:
        id_getter = self._create_value_getter(self.primary_id_expr)
        source_getter = self._create_value_getter(self.source_expr)
        target_getter = self._create_value_getter(self.target_expr)
        label_getters = [self._create_value_getter(label) for label in self.labels_expr]
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr] + [
            self._create_key_value_getter((LiteralExpression(prop[0]), LiteralExpression(prop[1])))
            for prop in context.static_properties
        ]

        for data in data_stream:
            yield EdgeInfo(
                id=id_getter(data),
                source_id=source_getter(data),
                target_id=target_getter(data),
                labels=[label_getter(data) for label_getter in label_getters],
                properties=[property_getter(data) for property_getter in property_getters],
            )
