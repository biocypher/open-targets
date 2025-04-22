"""Definition of data views."""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any, Protocol, TypeAlias, overload, runtime_checkable

from open_targets.data.schema_base import Field, SequenceField, StructField

DataViewPrimitiveValue: TypeAlias = str | int | float | bool
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
    the sequence.
    """

    def __init__(
        self,
        field_index_mapping: Mapping[type[Field], int],
        data: Sequence[Any],
        mapped_fields: Iterable[type[Field]],
    ) -> None:
        """Initialize the data view with raw data that is a sequence.

        Args:
            field_index_mapping: A mapping of field classes to their index in
                the sequence.
            data: The raw data.
            mapped_fields: The fields that the view will present.
        """
        self._field_index_mapping = field_index_mapping
        self._data = data
        self._mapped_fields = mapped_fields

    def __iter__(self) -> Iterator[type[Field]]:
        """Get the keys which are the field classes."""
        return iter(key for key in self._field_index_mapping if key in self._mapped_fields)

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._field_index_mapping)

    def __getitem__(self, key: type[Field]) -> DataViewValue:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a view is returned, otherwise
        the raw value is returned
        """
        value = self._data[self._field_index_mapping[key]]
        if issubclass(key, StructField):
            return MappingBackedDataView(value, key.fields)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataView(value, key.element.fields) if value is not None else []
        return value

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
        value = self._data[key.name]
        if issubclass(key, StructField):
            return MappingBackedDataView(value, key.fields)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataView(value, key.element.fields)
        return value

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data
