"""Data views for type-safe access to query results.

This module provides a set of classes and protocols for creating type-safe views
over data returned by queries. The views allow accessing data using field
classes as keys, eliminating the need to know the exact field names while
maintaining type safety.

If the accessed field is a leaf field, the raw value is returned. If the
accessed field is a nested field, an appropriate view is returned for chained
accesses.

Views are exposed as mappings and sequences for easy use.
"""

from collections.abc import Iterator, Mapping, Sequence
from typing import Any, Protocol, TypeAlias, cast, overload, runtime_checkable

from open_targets.data.schema_base import Field, SequenceField, StructField

DataViewPrimitiveValue: TypeAlias = str | int | float | bool | None
DataView: TypeAlias = Mapping[
    type[Field],
    "DataViewPrimitiveValue | DataView | Sequence[DataViewPrimitiveValue | DataView]",
]
DataViewValue: TypeAlias = "DataViewPrimitiveValue | DataView | Sequence[DataViewPrimitiveValue | DataView]"


@runtime_checkable
class DataViewProtocol(Protocol):
    """Protocol for data views for data returned by a query.

    Data views inherit from mappings and sequences and can be accessed via the
    field class, eliminating the need to know the field name to ensure type
    safety.
    """

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""


class ArrayDataView(DataViewProtocol, Sequence[DataView]):
    """Data view for raw data that is a sequence."""

    def __init__(self, data: Sequence[dict[str, Any]], element_fields: Sequence[type[Field]]) -> None:
        """Initialize the data view with raw data that is a sequence.

        Args:
            data: The raw data.
            element_fields: The fields that the view of each element will
                present.
        """
        self._data = data
        self._element_fields = element_fields

    def __iter__(self) -> Iterator[DataView]:
        """Iterate over the sequence."""
        return (MappingBackedDataView(x, self._element_fields) for x in self._data)

    @overload
    def __getitem__(self, index: int) -> DataView: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[DataView]: ...

    def __getitem__(
        self,
        index: int | slice,
    ) -> DataView | Sequence[DataView]:
        """Access in sequence protocol with items returned as views."""
        if isinstance(index, int):
            return MappingBackedDataView(self._data[index], self._element_fields)
        return [MappingBackedDataView(item, self._element_fields) for item in self._data[index]]

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._data)

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data


class SequenceBackedDataView(DataViewProtocol, DataView):
    """Data view for raw data that is a sequence.

    A dictionary is needed to map the field class to the index of the data in
    the sequence. This view also supports virtual keys which access nested
    fields directly. A virtual key is a field class that translates to a
    sequence of fields which are used to access a nested structure in the
    data. When a virtual key is accessed, the view is recursively created.

    For instance, a field index mapping and corresponding data could be:
    field_index_mapping = {
        FieldA: 0,
        FieldB: 1,
        FieldC: [FieldB, FieldC],
    }
    data = (
        123,
        {
            "FieldC": "value",
        },
    )
    As a result, the following access is allowed:
    view[FieldA] -> 123
    view[FieldB] -> { "FieldC": "value" }
    view[FieldC] -> "value"
    """

    def __init__(
        self,
        field_path_mapping: Mapping[type[Field], int | Sequence[type[Field]]],
        data: Sequence[Any],
        mapped_fields: Sequence[type[Field]],
    ) -> None:
        """Initialize the data view with raw data that is a sequence.

        Args:
            field_index_mapping: A mapping of field classes to their index in
                the sequence.
            data: The raw data.
            mapped_fields: The fields that the view will present.
        """
        self._field_path_mapping = field_path_mapping
        self._data = data
        self._mapped_fields = mapped_fields

    def __iter__(self) -> Iterator[type[Field]]:
        """Get the keys which are the field classes."""
        return iter(self._mapped_fields)

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._mapped_fields)

    def __getitem__(self, key: type[Field]) -> DataViewValue:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a view is returned, otherwise
        the raw value is returned
        """
        path = self._field_path_mapping[key]
        if isinstance(path, int):
            return _create_view_value(self._data[path], key)
        return self._deep_create_view_value(self._data, path)

    def _deep_create_view_value(
        self,
        data: Any,
        path: Sequence[type[Field]],
    ) -> DataViewValue:
        field = cast("type[Field]", None)
        for field in path:
            if data is None:
                if issubclass(field, SequenceField):
                    return []
                return None
            if isinstance(data, Mapping):
                data = data.get(field.name)
            elif isinstance(data, Sequence):
                data = data[cast("int", self._field_path_mapping[field])]
            else:
                msg = f"Path {path} involves non-container field {field} in the middle."
                raise KeyError(msg)
        return _create_view_value(data, field)

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data


class MappingBackedDataView(DataViewProtocol, DataView):
    """Data view for raw data that is a mapping.

    Args:
        data: The raw data.
        mapped_fields: The fields that the view will present.
    """

    def __init__(self, data: Mapping[str, Any], mapped_fields: Sequence[type[Field]]) -> None:
        """Initialize the data view with raw data that is a mapping."""
        self._data = data
        self._mapped_fields = mapped_fields

    def __iter__(self) -> Iterator[type[Field]]:
        """Get the keys from the mapped fields."""
        return (field for field in self._mapped_fields if field.name in self._data)

    def __len__(self) -> int:
        """Get the length of the mapping."""
        return len(self._data)

    def __getitem__(self, key: type[Field]) -> DataViewValue:
        """Get the value by using field classes as keys.

        If the accessed value is not a leaf value, a view is returned,
        otherwise the raw value is returned
        """
        path = key.name
        return _create_view_value(self._data[path], key)

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data


def _create_view_value(data: Any, field: type[Field]) -> DataViewValue:
    if issubclass(field, StructField):
        return MappingBackedDataView(data, field.fields)
    if issubclass(field, SequenceField) and issubclass(field.element, StructField):
        return ArrayDataView(data if data is not None else [], field.element.fields)
    return data
