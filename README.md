# OTAR-BioCypher

This is a collection of [BioCypher](https://biocypher.org) adapters and
corresponding scripts for Open Targets data. It is a work in progress.

## Installation

The project uses [Poetry](https://python-poetry.org). You can install it like
this:

```
git clone https://github.com/saezlab/OTAR-BioCypher.git
cd OTAR-BioCypher
poetry install
```

Poetry will create a virtual environment according to your configuration (either
centrally or in the project folder). You can activate it by running `poetry
shell` inside the project directory. Alternatively, you can use a different
package manager to install the dependencies listed in `pyproject.toml`.

### Note about pycurl

You may encounter an error in executing the script combining this adapter and
the UniProt adapter about the SSL backend in pycurl: `ImportError: pycurl:
libcurl link-time ssl backend (openssl) is different from compile-time ssl
backend (none/other)`

Should this happen, it can be fixed as described here:
https://stackoverflow.com/questions/68167426/how-to-install-a-package-with-poetry-that-requires-cli-args
by running `poetry shell` followed by `pip list`, noting the version of pycurl,
and then running `pip install --compile --install-option="--with-openssl"
--upgrade --force-reinstall pycurl==<version>` to provide the correct SSL
backend.

## Open Targets target-disease associations

Target-disease association evidence is available from the Open Targets website
at https://platform.opentargets.org/downloads. The data can be downloaded in
Parquet format, which is a columnar data format that is compatible with Spark
and other big data tools. Currently, the data have to be manually downloaded
(e.g. using the wget command supplied on the website) and placed in the
`data/ot_files` directory. The adapter was created using version 22.11 of the
data.

To transfer the columnar data to a knowledge graph, we use the adapter in
`adapters/target_disease_evidence_adapter.py`, which is called from the script
`scripts/target_disease_script.py`. This script produces a set of
BioCypher-compatible files in the `biocypher-out` directory. To create the
knowledge graph from these files, you can find a version of the neo4j-admin
import command for the processed data in each individual output folder, under
the file name `neo4j-admin-import-call.sh`, which simply needs to be executed in
the home directory of the target database. More information about the BioCypher
package can be found at https://biocypher.org.

Please note that, by default, the adapter will be in `test mode`, which means
that it will only process a small subset of the data. To process the full data,
you can set the `test_mode` parameter in the adapter to `False` (or remove it).

### Adapter combination: UniProt and Dependency Map

To demonstrate the combination of multiple adapters to yield a single harmonised
knowledge graph, we add the [UniProt
adapter](https://github.com/HUBioDataLab/CROssBAR-BioCypher-Migration) (created
in the context of the CROssBAR v2 project) and the [Dependency Map
adapter](https://github.com/saezlab/DepMap-BioCypher) to the target-disease
knowledge graph creation script. The resulting script is
`scripts/target_disease_script_extended.py`.

Please note that while the UniProt adapter downloads data directly from UniProt
through pypath, the Dependency Map adapter is only functional for demonstration
purposes, as it requires the availability of local data (which is limited to
100 entries for our demo case).

### Docker version
To use start a dockerized neo4j database which will automatically load and build 
the database of this repository, `docker` and `docker compose` (formerly 
`docker-compose`) need to be installed. Build the container using `docker-compose 
build` and run `docker-compose up -d` to start it.

## Barrio-Hernandez et al. 2021 graph dump

Barrio-Hernandez and colleagues used interaction data from the Open Targets
platform to implement their method of network expansion
(https://www.biorxiv.org/content/10.1101/2021.07.19.452924v1). A dump file of
the Neo4j knowledge graph they used is available at
http://ftp.ebi.ac.uk/pub/databases/intact/various/ot_graphdb/current/.

Once successfully installed, porting the OTAR graph can be attempted by running
a local (or remotely accesssible) instance of the OTAR graph dump in Neo4j and
executing the Python script at `scripts/barrio_hernandez_script.py`. This will
connect to BioCypher using the adapter (from
`adapters/barrio_hernandez_adapter.py`) and write the BioCypher-compatible
structured data to the `biocypher-out` directory. You can find a version of the
neo4j-admin import command for the processed data in each individual output
folder, under the file name `neo4j-admin-import-call.sh`, which simply needs to
be executed in the home directory of the target database. More information about
the BioCypher package can be found at https://biocypher.org.
