from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

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


class GenerationDefinition(Generic[TGraphComponent], ABC):
    @abstractmethod
    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""

    @abstractmethod
    def generate(self, context: GenerationContext) -> Iterable[TGraphComponent]:
        """Generate graph components by directly accessing the context."""


@dataclass(frozen=True)
class ScanningGenerationDefinition(
    GenerationDefinition[TGraphComponent],
    ABC,
):
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
    ) -> Iterable[TGraphComponent]:
        pass

    @property
    @abstractmethod
    def scan_operation(self) -> ScanOperation:
        """Scan operation that is used to generate the graph components."""

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


class ExpressionNodeGenerationDefinitionBase(ExpressionGenerationDefinition[NodeInfo], ABC):
    """Definition of a set of nodes to be generated."""

    @property
    @abstractmethod
    def primary_id_expr(self) -> Expression[str]:
        """Expression that is used to get the primary id of the node."""

    @property
    @abstractmethod
    def labels_expr(self) -> Sequence[Expression[str]]:
        """Expressions that are used to get the labels of the node."""

    @property
    @abstractmethod
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        """Expressions that are used to get the properties of the node."""

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
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr]

        for data in data_stream:
            yield NodeInfo(
                id=id_getter(data),
                labels=[label_getter(data) for label_getter in label_getters],
                properties=[property_getter(data) for property_getter in property_getters],
            )


class ExpressionEdgeGenerationDefinitionBase(ExpressionGenerationDefinition[EdgeInfo], ABC):
    """Definition of a set of edges to be generated."""

    @property
    @abstractmethod
    def primary_id_expr(self) -> Expression[str]:
        """Expression that is used to get the primary id of the node."""

    @property
    @abstractmethod
    def source_expr(self) -> Expression[str]:
        """Expression that is used to get the source of the edge."""

    @property
    @abstractmethod
    def target_expr(self) -> Expression[str]:
        """Expression that is used to get the target of the edge."""

    @property
    @abstractmethod
    def labels_expr(self) -> Sequence[Expression[str]]:
        """Expressions that are used to get the labels of the node."""

    @property
    @abstractmethod
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        """Expressions that are used to get the properties of the node."""

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
        property_getters = [self._create_key_value_getter(prop) for prop in self.properties_expr]

        for data in data_stream:
            yield EdgeInfo(
                id=id_getter(data),
                source_id=source_getter(data),
                target_id=target_getter(data),
                labels=[label_getter(data) for label_getter in label_getters],
                properties=[property_getter(data) for property_getter in property_getters],
            )


@dataclass(frozen=True, kw_only=True)
class ExpressionNodeGenerationDefinition(ExpressionNodeGenerationDefinitionBase):
    primary_id: Expression[str]
    labels: Sequence[Expression[str]]
    properties: Sequence[tuple[Expression[str], Expression[str]]]

    @property
    def primary_id_expr(self) -> Expression[str]:
        return self.primary_id

    @property
    def labels_expr(self) -> Sequence[Expression[str]]:
        return self.labels

    @property
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return self.properties


@dataclass(frozen=True, kw_only=True)
class ExpressionEdgeGenerationDefinition(ExpressionEdgeGenerationDefinitionBase):
    primary_id: Expression[str]
    source: Expression[str]
    target: Expression[str]
    labels: Sequence[Expression[str]]
    properties: Sequence[tuple[Expression[str], Expression[str]]]

    @property
    def primary_id_expr(self) -> Expression[str]:
        return self.primary_id

    @property
    def source_expr(self) -> Expression[str]:
        return self.source

    @property
    def target_expr(self) -> Expression[str]:
        return self.target

    @property
    def labels_expr(self) -> Sequence[Expression[str]]:
        return self.labels

    @property
    def properties_expr(self) -> Sequence[tuple[Expression[str], Expression[str]]]:
        return self.properties


class SimpleNodeGenerationDefinitionMixin:
    def _to_expression(self, value: str | type[Field]) -> Expression[Any]:
        if isinstance(value, str):
            return LiteralExpression(value)
        return FieldExpression(value)


@dataclass(frozen=True, kw_only=True)
class SimpleNodeGenerationDefinition(SimpleNodeGenerationDefinitionMixin, ExpressionNodeGenerationDefinitionBase):
    primary_id: str | type[Field]
    labels: Sequence[str | type[Field]]
    properties: Sequence[type[Field] | tuple[str | type[Field], str | type[Field]]]

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


@dataclass(frozen=True, kw_only=True)
class SimpleEdgeGenerationDefinition(SimpleNodeGenerationDefinitionMixin, ExpressionEdgeGenerationDefinitionBase):
    primary_id: str | type[Field]
    source: str | type[Field]
    target: str | type[Field]
    labels: Sequence[str | type[Field]]
    properties: Sequence[type[Field] | tuple[str | type[Field], str | type[Field]]]

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
