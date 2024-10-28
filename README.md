# Open Targets BioCypher KG

This the [BioCypher](https://biocypher.org) prototype for adapting Open Targets
platform data. It is a work in progress.

## Installation

The project uses [Poetry](https://python-poetry.org). You can install it like
this:

```
git clone https://github.com/biocypher/open-targets.git
cd open-targets
poetry install
```

Poetry will create a virtual environment according to your configuration (either
centrally or in the project folder). You can activate it by running `poetry
shell` inside the project directory. Alternatively, you can use a different
package manager to install the dependencies listed in `pyproject.toml`.

## Open Targets target-disease associations

Target-disease association evidence is available from the Open Targets website
at https://platform.opentargets.org/downloads. The data can be downloaded in
Parquet format, which is a columnar data format that is compatible with Spark
and other big data tools. Currently, the data have to be manually downloaded
(e.g. using the wget command supplied on the website) and placed in the
`data/ot_files` directory. The adapter currently supports version 23.02 of the
data. Available datasets: `Target`, `Disease/Phenotype`, `Drug`, `Target - gene
ontology`, `Target - mouse phenotypes` and `Target - Disease Evidence`. CAVE:
The latter, which is the main source of target-disease interactions in the open
targets platform, is provided in two links, one for the literature evidence
(`literature/evidence`) and one for the full aggregated set (simply `evidence`).
The adapter uses the full set, so make sure to download the correct one. The
scripts directory contains a `parquet_download.sh` script that can be used to
download the files (make sure to execute it in the correct folder,
`data/ot_files`).

To transfer the columnar data to a knowledge graph, we use the adapter in
`otar_biocypher/target_disease_evidence_adapter.py`, which is called from the
script `scripts/target_disease_script.py`. This script produces a set of
BioCypher-compatible files in the `biocypher-out` directory. To create the
knowledge graph from these files, you can find a version of the neo4j-admin
import command for the processed data in each individual output folder, under
the file name `neo4j-admin-import-call.sh`, which simply needs to be executed in
the home directory of the target database. More information about the BioCypher
package can be found at https://biocypher.org.

Please note that, by default, the adapter will be in `test mode`, which means
that it will only process a small subset of the data. To process the full data,
you can set the `test_mode` parameter in the adapter to `False` (or remove it).
