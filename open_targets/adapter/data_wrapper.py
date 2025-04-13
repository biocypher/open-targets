"""Definition of data wrappers."""

from abc import ABC
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, TypeAlias, overload

from open_targets.data.schema_base import Field, SequenceField, StructField

ConvertedType: TypeAlias = "str | int | float | bool | DataWrapper | Sequence[ConvertedType]"


class DataWrapper(Mapping[type[Field], ConvertedType], ABC):
    """Interface class for data wrappers for nested data.

    Data wrapped behaves like a mapping and can be accessed via the field class,
    eliminating the need to know the field name to ensure type safety.
    """


class ArrayDataWrapper(Sequence[DataWrapper], ABC):
    """Data wrapper for sequence types of data."""

    def __init__(self, data: Sequence[dict[str, Any]]) -> None:
        """Initialize the data wrapper with array data."""
        self._data = data

    def __iter__(self) -> Iterator[DataWrapper]:
        """Iterate over the sequence."""
        return (MappingPresentingDataWrapper(x) for x in self._data)

    @overload
    def __getitem__(self, index: int) -> DataWrapper: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[DataWrapper]: ...

    def __getitem__(self, index: int | slice) -> DataWrapper | Sequence[DataWrapper]:
        """Access the array like a typical sequence but results are wrapped."""
        if isinstance(index, int):
            return MappingPresentingDataWrapper(self._data[index])
        return [MappingPresentingDataWrapper(item) for item in self._data[index]]

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._data)


class SequencePresentingDataWrapper(DataWrapper):
    """Data wrapper for data that is represented as a sequence.

    A dictionary is needed to map the field class to the index of the data in
    the sequence.
    """

    def __init__(self, field_index_dict: Mapping[type[Field], int], data: Sequence[Any]) -> None:
        """Initialize the data wrapper with data represented as a sequence.

        An additional mapping is needed for converting field classes to indexes.
        """
        self._field_index_dict = field_index_dict
        self._data = data

    def __iter__(self) -> Iterator[type[Field]]:
        """Get the keys which are the field classes."""
        return iter(self._field_index_dict)

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._field_index_dict)

    def __getitem__(self, key: type[Field]) -> ConvertedType:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a wrapper is returned,
        otherwise the raw value is returned
        """
        value = self._data[self._field_index_dict[key]]
        if issubclass(key, StructField):
            return MappingPresentingDataWrapper(value)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataWrapper(value) if value is not None else []
        return value


class MappingPresentingDataWrapper(DataWrapper):
    """Data wrapper for data that is represented as a mapping.

    The name in a field class can be used directly to access the data.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize the data wrapper with data represented as a mapping."""
        self._data = data

    def __iter__(self) -> Iterator[type[Field]]:
        """Not yet implemented.

        Due to the need to convert keys to field classes which is not efficient,
        this is postponed.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Get the length of the dictionary."""
        return len(self._data)

    def __getitem__(self, key: type[Field]) -> ConvertedType:
        """Get the data by using field classes as keys.

        If the access value is not a leaf value, a wrapper is returned,
        otherwise the raw value is returned
        """
        value = self._data[key.name]
        if issubclass(key, StructField):
            return MappingPresentingDataWrapper(value)
        if issubclass(key, SequenceField) and issubclass(key.element, StructField):
            return ArrayDataWrapper(value)
        return value
