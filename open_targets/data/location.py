"""Resolve dataset repository locations for local and remote access."""

from os import PathLike
from pathlib import Path
from urllib.parse import unquote, urlparse

from open_targets.data.schema_base import Dataset

FILE_SCHEME = "file"
S3_SCHEME = "s3"
LOCAL_FILE_NETLOCS = frozenset({"", "localhost"})


def resolve_datasets_location(
    datasets_location: str | PathLike[str],
) -> tuple[bool, str]:
    """Resolve a dataset location into a remote flag and a base location.

    Args:
        datasets_location: A local path, a ``file://`` URL, or an ``s3://``
            repository root.

    Returns:
        tuple[bool, str]: Whether the location is remote and the base location
        used to build dataset paths.

    Raises:
        ValueError: If the location uses an unsupported URL scheme or an
            invalid file URL.
    """
    if isinstance(datasets_location, PathLike):
        return False, _normalise_local_path(datasets_location)

    location = str(datasets_location)
    if "://" not in location:
        return False, _normalise_local_path(location)

    parsed = urlparse(location)
    scheme = parsed.scheme.lower()

    if scheme == FILE_SCHEME:
        if parsed.netloc not in LOCAL_FILE_NETLOCS:
            msg = f"Only local file URLs are supported: {location}"
            raise ValueError(msg)
        if not parsed.path:
            msg = f"File URL must include a path: {location}"
            raise ValueError(msg)
        return False, _normalise_local_path(unquote(parsed.path))

    if scheme == S3_SCHEME:
        if not parsed.netloc:
            msg = f"S3 dataset location must include a bucket: {location}"
            raise ValueError(msg)
        base_location = f"{S3_SCHEME}://{parsed.netloc}{parsed.path}"
        return True, base_location.rstrip("/")

    msg = (
        f"Unsupported dataset location scheme '{scheme}'. "
        "Supported schemes are 'file' and 's3', or provide a local path."
    )
    raise ValueError(msg)


def build_dataset_path(
    base_location: str,
    dataset: type[Dataset],
    *,
    remote: bool,
) -> str:
    """Build the parquet glob path for a dataset.

    Args:
        base_location: The local directory or remote repository root.
        dataset: The dataset whose files should be located.
        remote: Whether the base location is remote.

    Returns:
        str: The parquet glob path for the dataset.
    """
    if remote:
        return f"{base_location.rstrip('/')}/{dataset.id}/**/*.parquet"
    return str(Path(base_location) / dataset.id / "**" / "*.parquet")


def _normalise_local_path(location: str | PathLike[str]) -> str:
    """Normalise a local path to a string."""
    return str(Path(location))
