# BioCypher Open Targets Data (24.09) Adapter

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This repository contains a [BioCypher](https://biocypher.org) adapter for adapting Open Targets data at version 24.09. The project is currently under heavy development.

## Overview

BioCypher's modular design allows it to use different adapters to consume different kinds of data sources to produce knowledge graphs. This adapter is a primary adapter for adapting [Open Targets data](https://platform.opentargets.org/downloads). The adapter also comes with presets of node of entities and edges of relationships. A script is provided for running BioCypher with the adapter to create a knowledge graphs with all predefined nodes and edges included. On a consumer laptop it would takes 1-2 hours to build the full graph.

## Features

- Converts Open Targets data (version 24.09) into BioCypher-compatible format
- Presets of nodes and edges
- Declarative syntax to minimise the code needed to construct the desired graph schema
- Backed by [duckdb](https://duckdb.org/) which makes the adapter fast and memory efficient
- True streaming from datasets to BioCypher, almost no intermediate memory pressure

## Node and Edge Presets
### Node
- Target
- Disease
- Gene Ontology
- Molecule
- Mouse Model
- Mouse Phenotype
- Mouse Target

### Edge
- Target -> Disease
- Target -> Gene Ontology

## Prerequisites

- [Poetry](https://python-poetry.org) for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/biocypher/open-targets.git
   cd open-targets
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

4. The adapter can now be imported:
   ```python
   from open_targets.adapter import acquisition_context
   ```

## Data Preparation
Required datasets by node/edge definition presets:
- (Target)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/targets/]
- (Disease)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/diseases/]
- (Molecule)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/molecule/]
- (Gene Ontology)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/molecule/]
- (Mouse Phenotypes)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/mousePhenotypes/]
- (Evidence)[https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/evidence/]

The resulted directory should have the following structure.
directory-of-your-choice/
├── targets/
│   └── **
│       └── *.parquet
├── diseases/
│   └── **
│       └── *.parquet
...

## Usage
### Quick Start
1. Follows [Data Preparation](#data-preparation) and place the downloaded Parquet files in the `data/ot_files` directory

2. Run the script.
```bash
python ./scripts/open_targets_biocypher_run.py
```
The script runs BioCypher and generates a knowledge graph using all our node/edge definition presets.

### Not So Quick Start
Basically the [Quick Start](#quick-start) but with your own set of node/edge definiiton presets.
```python
    from open_targets.definition import (
        ...
    )

    bc = BioCypher(biocypher_config_path=...)

    node_definitions = ... # imported node definitions
    edge_definitions = ... # imported edge definitions

    context = AcquisitionContext(
        node_definitions=node_definitions,
        edge_definitions=edge_definitions,
        datasets_location=..., # directory where you placed the downloaded datasets.
    )

    for node_definition in node_definitions:
        bc.write_nodes(context.get_acquisition_generator(node_definition))
    for edge_definition in edge_definitions:
        bc.write_edges(context.get_acquisition_generator(edge_definition))
```
In short, a context is fisrt constrcuted by providing a set of node/edge definitions, then, for each definition you can get a generator which will stream data from a dataset to BioCypher. The data querying and transformation is defined in a node/edge definition.

More detail for customisation is down below.

## Open Targets Data Schema
The full schema of Open Targets data is represented as Python classes which are included in this adapter. The intention is to provide type checking of dataset or field referencing in code to minimise human error. All dataset or field classes could be found in `open_targets/data/schema.py`.

All dataset and field classes' names start with `Dataset` and `Field` correspondingly. Names of fields follow their structural location in their datasets. For instance, `FieldTargetsHallmarksAttributes` is a field named `attributes` in dataset `targets`, under the field `hallmarks`.

The schema could be used for data discovery and is used in node/edge definition.

## Custom Node/Edge Definitions
A node/edge definition describes how nodes/edges are acquired from a dataset. Each node/edge has essential attributes for it to be a valid graph component and a definition tells how the values of them are acquired/computed. Each attribute has an expression assigned describing the chain of actions to acquire the value from the dataset. An expression could be as simple as a field access or a chained transformation. The following is a simple definition.

```python
definition = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTargets),
    primary_id=FieldExpression(FieldTargetsId),
    label=LiteralExpression("ensembl"),
    properties=[
        (LiteralExpression(FieldTargetsApprovedSymbol.name), FieldExpression(FieldTargetsApprovedSymbol))
    ],
)
```
In natural language, the dataset `targets` will be scaned through and for each row, a node is generated with it's id assigned with the value from field `id` and it's label assigned with a literal value `ensembl` and it's properties appended with only one property in which it's key and value being the name of the referenced field `approvedSymbol` and the value from the field correspondingly.

Expressions could be chained together:
```python
expression = NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldEvidenceDiseaseId)))
```
Which is equivalent to
```python
value = normalise_curie(str(data[FieldEvidenceDiseaseId]))
```
In fact, this is almost exactly the built and cached function that will be run during an acquisition.

An edge definition is similar but with two extra attributes `source` and `target` to link two nodes together.

For slight customisation, you can derive one from on of our preset as follows.
```python
from open_targets.data.schema import FieldTargetsApprovedSymbol
from open_targets.definition import node_target
from dataclasses import replace
node_definition = replace(node_target, primary_id=FieldTargetsApprovedSymbol)
```

## Code Generation
This repository makes use of code generation (powered by (jinja)[https://jinja.palletsprojects.com/en/stable/]) to generate some scripts such as the Open Targets data schema represented in Python classes. The code generation scripts are under `code_generation`. `*.jinja` are template files of the generated scripts and each one will have it's corresponding script generated in the same directory it resides.

## Future
- Streaming from cloud, eliminating the need of downloading datasets to local storage
- Codeless mode, defining node/edge definitions in a JSON/YAML file
- Reach beyond Open Targets data to covers all kinds of tabular data
- Comprehensive set of scientifically meaningful node/edge definitions and knowledge graph schemas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or an Issue if you discovered any issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
