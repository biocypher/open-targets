import pytest

from open_targets.data.metadata._fetch import fetch_open_targets_dataset_metadatas
from open_targets.data.metadata.model import OpenTargetsDatasetFormat


@pytest.mark.parametrize(
    ("filter_dataset_ids", "filter_format", "expected_number_of_datasets"),
    [
        (["targets"], None, 2),
        (["targets"], [OpenTargetsDatasetFormat.PARQUET], 1),
        (None, None, 68),
    ],
)
def test_fetch_open_targets_dataset_metadatas(
    filter_dataset_ids: list[str],
    filter_format: list[OpenTargetsDatasetFormat] | None,
    expected_number_of_datasets: int,
) -> None:
    metadatas = fetch_open_targets_dataset_metadatas(filter_dataset_ids, filter_format)
    assert len(metadatas) == expected_number_of_datasets
