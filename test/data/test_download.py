from open_targets.data.download import get_dataset_download_urls
from open_targets.data.metadata._fetch import fetch_open_targets_dataset_metadatas
from open_targets.data.metadata.model import OpenTargetsDatasetFormat


def test_get_dataset_download_urls() -> None:
    metadata = fetch_open_targets_dataset_metadatas(["drugWarnings"], [OpenTargetsDatasetFormat.PARQUET])[0]
    urls = get_dataset_download_urls(metadata)
    expected_urls = [
        "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/22.11/output/etl/parquet/drugWarnings/_SUCCESS",
        "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/22.11/output/etl/parquet/drugWarnings/part-00000-1b649df2-49a0-4139-971c-0229a95373f3-c000.snappy.parquet",
    ]
    assert sorted(urls) == sorted(expected_urls)
