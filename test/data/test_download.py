from open_targets.config import DATA_VERSION
from open_targets.data.download import get_dataset_download_urls
from open_targets.data.metadata._fetch import fetch_open_targets_dataset_metadata
from open_targets.data.metadata.model import OpenTargetsDatasetFormat


def test_get_dataset_download_urls() -> None:
    metadata = fetch_open_targets_dataset_metadata(["drugWarnings"], [OpenTargetsDatasetFormat.PARQUET])[0]
    urls = get_dataset_download_urls(metadata)
    expected_urls = [
        f"https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/{DATA_VERSION}/output/etl/parquet/drugWarnings/_SUCCESS",
        f"https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/{DATA_VERSION}/output/etl/parquet/drugWarnings/part-00000-da958cfc-89ba-4519-80a4-6b32e6283755-c000.snappy.parquet",
    ]
    assert sorted(urls) == sorted(expected_urls)
