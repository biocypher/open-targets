"""Definition of acquisition definitions.

Acquisition definitions also define the actual logic querying the datasets.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeAlias, TypeVar

from typing_extensions import override

from open_targets.adapter._helper._acquisition_definition import recursive_build_expression_function
from open_targets.adapter._helper._expression import recursive_get_dependent_fields, to_expression
from open_targets.adapter.context_protocol import AcquisitionContextProtocol
from open_targets.adapter.data_view import DataView
from open_targets.adapter.expression import (
    Expression,
)
from open_targets.adapter.output import EdgeInfo, NodeInfo
from open_targets.adapter.scan_operation import ExplodingScanOperation, ScanOperation
from open_targets.data.schema import Field
from open_targets.data.schema_base import Dataset

Source: TypeAlias = int | float | str | type[Field] | Expression[Any]
TAcqusitionOutput = TypeVar("TAcqusitionOutput")


class AcquisitionDefinition(Generic[TAcqusitionOutput], ABC):
    """Base class for all acquisition definitions.

    An acquisition definition describes how to acquire a set of nodes/edges.
    High level definitions are provided but in the case of more complex
    acquisition logic, a subclass of this class can be used to query the
    dataset directly to provide the specific logic.
    """

    @abstractmethod
    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""

    @abstractmethod
    def acquire(self, context: AcquisitionContextProtocol) -> Iterable[TAcqusitionOutput]:
        """Acquire graph components by directly accessing the context."""


class ScanningAcquisitionDefinition(
    AcquisitionDefinition[TAcqusitionOutput],
    ABC,
):
    """Acquisition definition that uses a scan operation to acquire.

    The dataset query is abstracted out by the scan operation which determines
    the fashion of data query. Items yielded are data views for easy access
    to the data fields.
    """

    @abstractmethod
    def _get_scan_operation(self) -> ScanOperation:
        """Scan operation that is used to acquire the graph components."""

    @abstractmethod
    def _get_required_fields(self) -> Iterable[type[Field]]:
        """Fields that are requested by this definition."""

    @abstractmethod
    def _acquire_from_scanning(
        self,
        context: AcquisitionContextProtocol,
        data_stream: Iterable[DataView],
    ) -> Iterable[TAcqusitionOutput]:
        """Acquire graph components from the scanning result stream."""

    @override
    def get_required_datasets(self) -> Iterable[type[Dataset]]:
        """Datasets that are required by this definition."""
        return {self._get_scan_operation().dataset}

    @override
    def acquire(self, context: AcquisitionContextProtocol) -> Iterable[TAcqusitionOutput]:
        """Create the scanning result stream from the low level access."""
        scan_result_stream = context.get_scan_result_stream(
            self._get_scan_operation(),
            list(self._get_required_fields()),
        )
        return self._acquire_from_scanning(context, scan_result_stream)


@dataclass(frozen=True)
class _ExpressionAcquisitionDefinition(
    ScanningAcquisitionDefinition[TAcqusitionOutput],
    ABC,
):
    """Acquisition definition that is described by expressions.

    Expressions are used to describe how to obtain values of the attributes of
    nodes or edges from a scanning result.
    """

    scan_operation: ScanOperation

    @property
    @abstractmethod
    def _all_expressions(self) -> Sequence[Expression[Any]]:
        """All expressions that are included in this definition."""

    @override
    def _get_scan_operation(self) -> ScanOperation:
        """Return the provided scan operation."""
        return self.scan_operation

    @override
    def _get_required_fields(self) -> Iterable[type[Field]]:
        """Get all fields that are required by all the expressions."""
        fields = set[type[Field]]()
        for expression in self._all_expressions:
            fields.update(recursive_get_dependent_fields(expression))
        if isinstance(self.scan_operation, ExplodingScanOperation):
            fields.add(self.scan_operation.exploded_field)
        return fields

    def _create_value_getter(
        self,
        expression: Expression[Any],
    ) -> Callable[[DataView], Any]:
        func = recursive_build_expression_function(expression)
        return lambda data: func(data)


@dataclass(frozen=True)
class ExpressionNodeAcquisitionDefinition(_ExpressionAcquisitionDefinition[NodeInfo]):
    """Expression acquisition definition for nodes."""

    scan_operation: ScanOperation
    primary_id: Source
    label: Source
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def _primary_id_expr(self) -> Expression[str]:
        return to_expression(self.primary_id)

    @property
    def _label_expr(self) -> Expression[str]:
        return to_expression(self.label)

    @property
    def _property_exprs(self) -> Sequence[tuple[Expression[str], Expression[Any]]]:
        return [
            (to_expression(prop[0]), to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (to_expression(prop.name), to_expression(prop))
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

    @override
    def _acquire_from_scanning(
        self,
        context: AcquisitionContextProtocol,
        data_stream: Iterable[DataView],
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
                logging.exception("Failed to acquire node from data: %s", data)


@dataclass(frozen=True)
class ExpressionEdgeAcquisitionDefinition(_ExpressionAcquisitionDefinition[EdgeInfo]):
    """Expression acquisition definition for edges."""

    primary_id: Source
    source: Source
    target: Source
    label: Source
    properties: Sequence[type[Field] | tuple[Source, Source]]

    @property
    def _primary_id_expr(self) -> Expression[str]:
        return to_expression(self.primary_id)

    @property
    def _source_expr(self) -> Expression[str]:
        return to_expression(self.source)

    @property
    def _target_expr(self) -> Expression[str]:
        return to_expression(self.target)

    @property
    def _label_expr(self) -> Expression[str]:
        return to_expression(self.label)

    @property
    def _property_exprs(self) -> Sequence[tuple[Expression[str], Expression[Any]]]:
        return [
            (to_expression(prop[0]), to_expression(prop[1]))
            if isinstance(prop, tuple)
            else (to_expression(prop.name), to_expression(prop))
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

    @override
    def _acquire_from_scanning(
        self,
        context: AcquisitionContextProtocol,
        data_stream: Iterable[DataView],
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
                logging.exception("Failed to acquire edge from data: %s", data)
