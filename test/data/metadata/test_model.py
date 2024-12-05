from typing import Final

import requests

from open_targets.data.metadata.model import _OpenTargetsDatasetMetadataModel

SCHEMA_URL: Final = "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.06/output/metadata/targets/part-00000-e02604eb-9c31-403c-8e02-804b58c9b41e-c000.json"


def test_open_targets_dataset_schema_model() -> None:
    json = requests.get(SCHEMA_URL, timeout=10).text
    schema = _OpenTargetsDatasetMetadataModel.model_validate_json(json)
    assert schema is not None
