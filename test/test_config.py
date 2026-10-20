from code_generation.config import flatten_config
from open_targets.config import DATA_REPOSITORY_URLS_S3


def test_s3_repository_url_is_emitted() -> None:
    assert DATA_REPOSITORY_URLS_S3.startswith("s3://")


def test_flatten_config_joins_nested_keys() -> None:
    config = {
        "data-version": "25.12",
        "data-repository-urls": {
            "ftp": "ftp://example.com/",
            "s3": "s3://example.com/",
        },
    }
    assert list(flatten_config(config)) == [
        ("DATA_VERSION", "25.12"),
        ("DATA_REPOSITORY_URLS_FTP", "ftp://example.com/"),
        ("DATA_REPOSITORY_URLS_S3", "s3://example.com/"),
    ]
