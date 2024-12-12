from io import BytesIO
from typing import Final

from open_targets import config
from open_targets.data._ftp_client import FTPClient
from open_targets.data.metadata.model import (
    OpenTargetsDatasetFormat,
    OpenTargetsDatasetMetadataModel,
)

HOST: Final = "ftp.ebi.ac.uk"
METADATA_PATH: Final = f"/pub/databases/opentargets/platform/{config.DATA_VERSION}/output/metadata"


def fetch_open_targets_dataset_metadatas(
    filter_dataset_ids: list[str] | None = None,
    filter_format: list[OpenTargetsDatasetFormat] | None = None,
) -> list[OpenTargetsDatasetMetadataModel]:
    """Fetch dataset metadatas from the Open Targets Platform FTP server.

    Args:
        filter_dataset_ids: If provided, only fetch metadata for the
        specified dataset IDs.

    Returns:
        A list of dataset metadatas.

    """
    ftp_client = FTPClient(HOST)
    metadata_dir_file_paths = ftp_client.traverse_directory(METADATA_PATH).files
    metadata_json_file_paths = [file_path for file_path in metadata_dir_file_paths if file_path.endswith(".json")]
    if filter_dataset_ids is not None:
        filters = [f"metadata/{dataset_id}" for dataset_id in filter_dataset_ids]
        metadata_json_file_paths = [
            file_path
            for file_path in metadata_json_file_paths
            if any(dataset_id in file_path for dataset_id in filters)
        ]

    jsons = list[bytes]()

    for file_path in metadata_json_file_paths:
        bytes_io = BytesIO()
        ftp_client.retrieve_file(file_path, bytes_io.write)
        jsons.append(bytes_io.getvalue())

    metadatas = [OpenTargetsDatasetMetadataModel.model_validate_json(json) for json in jsons]
    if filter_format is not None:
        metadatas = [metadata for metadata in metadatas if metadata.resource.format in filter_format]
    return metadatas
