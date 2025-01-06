"""Module providing functions to download Open Targets data."""

from typing import Final

from open_targets.config import DATA_VERSION, HOST
from open_targets.data._ftp_client import FTPClient
from open_targets.data.metadata.model import OpenTargetsDatasetMetadataModel

OUTPUT_PATH: Final = f"/pub/databases/opentargets/platform/{DATA_VERSION}/output/etl"


def get_dataset_download_urls(metadata: OpenTargetsDatasetMetadataModel) -> list[str]:
    """Get a list of download URLs of all files in a dataset."""
    directory_path = f"{OUTPUT_PATH}/{metadata.resource.format}/{metadata.resource.path.lstrip('/')}"
    discovered_files = FTPClient(HOST).traverse_directory(str(directory_path)).files
    return [f"https://{HOST}{file_path}" for file_path in discovered_files]
