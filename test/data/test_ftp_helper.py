from typing import Final, cast

import pytest

from open_targets.data._ftp_helper import FTPClient

HOST: Final[str] = "ftp.ebi.ac.uk"


@pytest.fixture
def ftp_client() -> FTPClient:
    return FTPClient(HOST)


def test_list_directory(ftp_client: FTPClient) -> None:
    path = "/pub/databases/opentargets/platform/22.11/input/webapp"
    expected_files = ["/pub/databases/opentargets/platform/22.11/input/webapp/downloads.json"]
    expected_dirs = ["/pub/databases/opentargets/platform/22.11/input/webapp/ontology"]
    result = ftp_client.list_directory(path)
    assert sorted(result.files) == sorted(expected_files)
    assert sorted(result.dirs) == sorted(expected_dirs)


def test_traverse_directory(ftp_client: FTPClient) -> None:
    path = "/pub/databases/opentargets/platform/22.11/input/webapp"
    expected_files = ["/pub/databases/opentargets/platform/22.11/input/webapp/downloads.json"]
    expected_dirs = [
        "/pub/databases/opentargets/platform/22.11/input/webapp/ontology",
        "/pub/databases/opentargets/platform/22.11/input/webapp/ontology/efo_json",
    ]
    result = ftp_client.traverse_directory(path, 1)
    assert sorted(result.files) == sorted(expected_files)
    assert sorted(result.dirs) == sorted(expected_dirs)


def test_retrieve_file(ftp_client: FTPClient) -> None:
    path = "/pub/databases/opentargets/platform/22.11/conf/22_11_2_platform.conf"
    expected_text = """// --- UPDATE THIS --- //
spark-settings.write-mode = "ignore"

data_version = "22.11.2"
chembl_version = "31"
ensembl_version = "108"
evidences.data-sources-exclude = ["ot_crispr", "encore", "ot_crispr_validation"]
# update defaults for next release
etl-dag.resolve = false
// --- END - UPDATE THIS --- //
common.input = "gs://open-targets-pre-data-releases/22.11.1/input"
epmc.input.cooccurences.format = "parquet"
epmc.input.cooccurences.path = "gs://open-targets-pre-data-releases/22.11/output/literature-etl/parquet/cooccurrences"

// include this to short-circuit calculation of literature step
literature.processing.outputs.literatureIndex.path = "gs://open-targets-pre-data-releases/22.11/literature-etl/parquet/"
"""
    result = cast(bytes, ftp_client.retrieve_file(path))
    text = result.decode()
    assert text == expected_text
