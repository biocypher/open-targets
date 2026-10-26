from pathlib import Path

import pytest

from open_targets.data.location import (
    build_dataset_path,
    resolve_datasets_location,
)
from open_targets.data.schema import DatasetTarget


@pytest.mark.parametrize(
    ("datasets_location", "expected"),
    [
        ("datasets", (False, "datasets")),
        (Path("datasets"), (False, "datasets")),
        ("file:///data/open-targets", (False, "/data/open-targets")),
        ("file:///data/open%20targets", (False, "/data/open targets")),
        ("s3://bucket/prefix/", (True, "s3://bucket/prefix")),
        ("s3://bucket", (True, "s3://bucket")),
    ],
)
def test_resolve_datasets_location(
    datasets_location: str | Path,
    expected: tuple[bool, str],
) -> None:
    assert resolve_datasets_location(datasets_location) == expected


@pytest.mark.parametrize(
    "datasets_location",
    [
        "ftp://example.com/data",
        "https://example.com/data",
    ],
)
def test_resolve_datasets_location_unsupported_scheme(datasets_location: str) -> None:
    with pytest.raises(ValueError, match=r"Unsupported|not supported"):
        resolve_datasets_location(datasets_location)


def test_resolve_datasets_location_requires_bucket() -> None:
    with pytest.raises(ValueError, match="bucket"):
        resolve_datasets_location("s3://")


def test_resolve_datasets_location_requires_local_file_url() -> None:
    with pytest.raises(ValueError, match="local file URLs"):
        resolve_datasets_location("file://remote-host/tmp/open-targets")


def test_build_dataset_path_local() -> None:
    expected = str(Path("/data/open-targets") / "target" / "**" / "*.parquet")
    assert build_dataset_path("/data/open-targets", DatasetTarget, remote=False) == expected


def test_build_dataset_path_remote() -> None:
    assert build_dataset_path("s3://bucket/prefix/", DatasetTarget, remote=True) == (
        "s3://bucket/prefix/target/**/*.parquet"
    )
