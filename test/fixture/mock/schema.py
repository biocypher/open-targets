from typing import Final

from open_targets.data.schema_base import Dataset, Field


def mock_dataset_factory(name: str) -> type[Dataset]:
    class MockDataset(Dataset):
        id: Final[str]  # type: ignore

    MockDataset.id = name  # type: ignore
    return MockDataset


def mock_field_factory(name: str) -> type[Field]:
    class MockField(Field):
        name: Final[str]  # type: ignore

    MockField.name = name  # type: ignore
    return MockField


MockDataset = mock_dataset_factory("mock_dataset")
MockField = mock_field_factory("mock_field")
