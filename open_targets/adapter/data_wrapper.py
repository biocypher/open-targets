from abc import ABC
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, TypeAlias, overload

from open_targets.data.schema_base import Field, SequenceField, StructField

ConvertedType: TypeAlias = "str | int | float | bool | DataWrapper | Sequence[ConvertedType]"


class DataWrapper(Mapping[type[Field], ConvertedType], ABC):
    pass


class ArrayDataWrapper(Sequence[DataWrapper], ABC):
    def __init__(self, data: Sequence[dict[str, Any]]) -> None:
        self._data = data

    def __iter__(self) -> Iterator[DataWrapper]:
        return (MappingPresentingDataWrapper(x) for x in self._data)

    @overload
    def __getitem__(self, index: int) -> DataWrapper: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[DataWrapper]: ...

    def __getitem__(self, index: int | slice) -> DataWrapper | Sequence[DataWrapper]:
        if isinstance(index, int):
            return MappingPresentingDataWrapper(self._data[index])
        return [MappingPresentingDataWrapper(item) for item in self._data[index]]

    def __len__(self) -> int:
        return len(self._data)


class SequencePresentingDataWrapper(DataWrapper):
    def __init__(self, field_index_dict: Mapping[type[Field], int], data: Sequence[Any]) -> None:
        self._field_index_dict = field_index_dict
        self._data = data

    def __iter__(self) -> Iterator[type[Field]]:
        return iter(self._field_index_dict)

    def __len__(self) -> int:
        return len(self._field_index_dict)

    def __getitem__(self, key: type[Field]) -> ConvertedType:
        value = self._data[self._field_index_dict[key]]
        if isinstance(key, StructField):
            return MappingPresentingDataWrapper(value)
        if isinstance(key, SequenceField) and isinstance(key.element_type, StructField):
            return ArrayDataWrapper(value)
        return value


class MappingPresentingDataWrapper(DataWrapper):
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def __iter__(self) -> Iterator[type[Field]]:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: type[Field]) -> ConvertedType:
        value = self._data[key.name]
        if isinstance(key, StructField):
            return MappingPresentingDataWrapper(value)
        if isinstance(key, SequenceField) and isinstance(key.element_type, StructField):
            return ArrayDataWrapper(value)
        return value
