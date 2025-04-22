"""Definition of data wrappers."""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any, TypeAlias, overload

from open_targets.data.schema_base import Field, SequenceField, StructField

Primitive: TypeAlias = str | int | float | bool
FieldMap: TypeAlias = Mapping[type[Field], "Primitive | FieldMap | Sequence[Primitive | FieldMap]"]
DataNode: TypeAlias = "Primitive | FieldMap | Sequence[Primitive | FieldMap]"


class DataWrapper(ABC):
    """Interface class for data wrappers for nested data.

    Data wrapped behaves like a mapping and can be accessed via the field class,
    eliminating the need to know the field name to ensure type safety.
    """

    @property
    @abstractmethod
    def raw_data(self) -> Any:
        """Get the raw data."""


class ArrayDataWrapper(DataWrapper, Sequence[FieldMap]):
    """Data wrapper for sequence types of data."""

    def __init__(self, data: Sequence[dict[str, Any]], element_fields: Sequence[type[Field]]) -> None:
        """Initialize the data wrapper with array data."""
        self._data = data
        self._element_fields = element_fields

    def __iter__(self) -> Iterator[FieldMap]:
        """Iterate over the sequence."""
        return (MappingPresentingDataWrapper(x, self._element_fields) for x in self._data)

    @overload
    def __getitem__(self, index: int) -> FieldMap: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[FieldMap]: ...

    def __getitem__(
        self,
        index: int | slice,
    ) -> FieldMap | Sequence[FieldMap]:
        """Access the array like a typical sequence but results are wrapped."""
        if isinstance(index, int):
            return MappingPresentingDataWrapper(self._data[index], self._element_fields)
        return [MappingPresentingDataWrapper(item, self._element_fields) for item in self._data[index]]

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._data)

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data


class SequencePresentingDataWrapper(DataWrapper, FieldMap):
    """Data wrapper for data that is represented as a sequence.

    A dictionary is needed to map the field class to the index of the data in
    the sequence.
    """

    def __init__(
        self,
        field_index_mapping: Mapping[type[Field], int],
        data: Sequence[Any],
        mapped_fields: Iterable[type[Field]],
    ) -> None:
        """Initialize the data wrapper with data represented as a sequence.

        An additional mapping is needed for converting field classes to indexes.
        The mapping may have more elements than the mapped fields which are not
        used.
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

    def __getitem__(self, key: type[Field]) -> DataNode:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a wrapper is returned,
        otherwise the raw value is returned
        """
        value = self._data[self._field_index_mapping[key]]
        if issubclass(key, StructField):
            return MappingPresentingDataWrapper(value, key.fields)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataWrapper(value, key.element.fields) if value is not None else []
        return value

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data


class MappingPresentingDataWrapper(DataWrapper, FieldMap):
    """Data wrapper for data that is represented as a mapping.

    The name in a field class can be used directly to access the data.
    """

    def __init__(self, data: Mapping[str, Any], mapped_fields: Sequence[type[Field]]) -> None:
        """Initialize the data wrapper with data represented as a mapping."""
        self._data = data
        self._mapped_fields = mapped_fields

    def __iter__(self) -> Iterator[type[Field]]:
        """Get the keys from the mapped fields."""
        return (field for field in self._mapped_fields if field.name in self._data)

    def __len__(self) -> int:
        """Get the length of the mapping."""
        return len(self._data)

    def __getitem__(self, key: type[Field]) -> DataNode:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a wrapper is returned,
        otherwise the raw value is returned
        """
        value = self._data[key.name]
        if issubclass(key, StructField):
            return MappingPresentingDataWrapper(value, key.fields)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataWrapper(value, key.element.fields)
        return value

    @property
    def raw_data(self) -> Any:
        """Get the raw data."""
        return self._data
