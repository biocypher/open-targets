from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from typing import Final

from open_targets import config
from open_targets.data._ftp_client import FTPClient
from open_targets.data.metadata.model import (
    OpenTargetsDatasetFormat,
    OpenTargetsDatasetMetadataModel,
    OpenTargetsDatasetSchemaModel,
)

HOST: Final = "ftp.ebi.ac.uk"
BASE_PATH: Final = f"/pub/databases/opentargets/platform/{config.DATA_VERSION}/output"


@dataclass(frozen=True)
class OpenTargetsDatasetVariantInfo:
    """Information of a dataset variant.

    Information of a dataset variant, usually a different format of the same
    dataset.
    """

    dataset_id: str
    path: str
    schema: OpenTargetsDatasetSchemaModel
    format: OpenTargetsDatasetFormat
    time_stamp: datetime


@dataclass(frozen=True)
class OpenTargetsDatasetInfo:
    """Information of a dataset.

    Information of a dataset inside a specific version of Open Targets Platform
    data.
    """

    id: str
    variants: list[OpenTargetsDatasetVariantInfo]


@dataclass
class OpenTargetsDataInfo:
    """Information of Open Targets Platform data.

    Information of a specific version of Open Targets Platform data.
    """

    version: str
    host: str
    path: str
    datasets: list[OpenTargetsDatasetInfo]


def get_open_targets_data_info() -> OpenTargetsDataInfo:
    """Get information about the targeted version of Open Targets Platform data.

    Search through the metadata JSON documents of the targeted version of data
    from the Open Targets Platform FTP server and return the result.
    """
    ftp_client = FTPClient(HOST)
    metadata_dir_file_paths = ftp_client.traverse_directory(f"{BASE_PATH}/metadata").files
    metadata_json_file_paths = [file_path for file_path in metadata_dir_file_paths if file_path.endswith(".json")]
    jsons = list[bytes]()

    for file_path in metadata_json_file_paths:
        bytes_io = BytesIO()
        ftp_client.retrieve_file(file_path, bytes_io.write)
        jsons.append(bytes_io.getvalue())

    return _convert_metadata_jsons_to_data_info(jsons)


def _convert_metadata_jsons_to_data_info(jsons: list[str] | list[bytes]) -> OpenTargetsDataInfo:
    deserialised_metadatas = list[OpenTargetsDatasetMetadataModel]()
    for json in jsons:
        deserialised = OpenTargetsDatasetMetadataModel.model_validate_json(json)
        deserialised_metadatas.append(deserialised)

    dataset_id_variant_info_map = dict[str, list[OpenTargetsDatasetVariantInfo]]()
    for deserialised_metadata in deserialised_metadatas:
        dataset_id = deserialised_metadata.id
        variant_info = OpenTargetsDatasetVariantInfo(
            dataset_id=dataset_id,
            path=BASE_PATH + f"/etl/{deserialised_metadata.resource.format}/{dataset_id}",
            schema=deserialised_metadata.dataset_schema,
            format=deserialised_metadata.resource.format,
            time_stamp=deserialised_metadata.time_stamp,
        )
        if dataset_id not in dataset_id_variant_info_map:
            dataset_id_variant_info_map[dataset_id] = []
        dataset_id_variant_info_map[dataset_id].append(variant_info)

    data_info = OpenTargetsDataInfo(
        version=config.DATA_VERSION,
        host=HOST,
        path=BASE_PATH,
        datasets=[],
    )

    for dataset_id, variant_infos in dataset_id_variant_info_map.items():
        dataset_info = OpenTargetsDatasetInfo(
            id=dataset_id,
            variants=variant_infos,
        )
        data_info.datasets.append(dataset_info)

    return data_info
