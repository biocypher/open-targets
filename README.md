# BioCypher Open Targets Data (24.09) Adapter

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This repository contains a [BioCypher](https://biocypher.org) adapter for Open
Targets data version 24.09. The project is currently under active development.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Node and Edge Types](#node-and-edge-types)
  - [Nodes](#nodes)
  - [Edges](#edges)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [Not So Quick Start](#not-so-quick-start)
- [Open Targets Data Schema](#open-targets-data-schema)
- [Custom Node/Edge Definitions](#custom-nodeedge-definitions)
- [Code Generation](#code-generation)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
- [License](#license)

## Overview

BioCypher's modular design enables the use of different adapters to consume
various data sources and produce knowledge graphs. This adapter serves as a
["secondary
adapter"](https://biocypher.org/latest/learn/tutorials/tutorial003_adapters/)
for [Open Targets data](https://platform.opentargets.org/downloads), meaning it
adapts a pre-harmonised composite of atomic resources via the Open Targets
pipeline. The adapter includes predefined sets of node types (entities) and edge
types (relationships), or in the language of this adapter, presets of node and
edge `definitions`. A script is provided to run BioCypher with the adapter,
creating a knowledge graph with all predefined nodes and edges. On a consumer
laptop, building the full graph typically takes 1-2 hours.

## Features

- Converts Open Targets data (version 24.09) into BioCypher-compatible format
- Includes predefined sets of node types and edge types (node and edge definition presets)
- Uses declarative syntax to minimize code needed for graph schema construction
- Powered by [duckdb](https://duckdb.org/) for fast and memory-efficient processing
- Implements true streaming from datasets to BioCypher with minimal intermediate memory usage

## Node and Edge Types
### Nodes
- Target
- Disease
- Gene Ontology (Category)
- Molecule
- Mouse Model
- Mouse Phenotype
- Mouse Target

### Edges
- Target -> Disease
- Target -> Gene Ontology
- Molecule -> Associated Target
- Molecule -> Associated Disease

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
Required datasets for node/edge definition presets:
- [Target](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/targets/)
- [Disease](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/diseases/)
- [Molecule](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/molecule/)
- [Gene Ontology](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/molecule/)
- [Mouse Phenotypes](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/mousePhenotypes/)
- [Evidence](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.09/output/etl/parquet/evidence/)

The resulting directory should have the following structure:
```
directory-of-your-choice/
├── targets/
│   └── **
│       └── *.parquet
├── diseases/
│   └── **
│       └── *.parquet
...
```

## Usage
### Quick Start
1. Follow the [Installation](#installation) steps

2. Follow the [Data Preparation](#data-preparation) steps and place the downloaded Parquet files in the `data/ot_files` directory

3. Run the script:
    ```bash
    python ./scripts/open_targets_biocypher_run.py
    ```
    The script runs BioCypher and generates a knowledge graph using all our node/edge definition presets.

### Not So Quick Start

Basically the [Quick Start](#quick-start) but with your own set of node/edge
definitions taken from our presets:

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
    datasets_location=..., # directory containing the downloaded datasets
)

for node_definition in node_definitions:
    bc.write_nodes(context.get_acquisition_generator(node_definition))
for edge_definition in edge_definitions:
    bc.write_edges(context.get_acquisition_generator(edge_definition))
```

In brief, first construct a context by providing a set of node/edge definitions.
Then, for each definition, you can obtain a generator that streams data from a
dataset to BioCypher. The data querying and transformation logic is defined in
the node/edge definitions.

More details about customization are provided below.

## Open Targets Data Schema

The full schema of Open Targets data is represented as Python classes included
in this adapter. This design provides type checking for dataset and field
references in code to minimize human error. All dataset and field classes can be
found in `open_targets/data/schema.py`.

All dataset and field classes are prefixed with `Dataset` and `Field`,
respectively. Field names follow their structural location in their datasets.
For example, `FieldTargetsHallmarksAttributes` represents the `attributes` field
in the `targets` dataset, under the `hallmarks` field.

The schema can be used for data discovery and is utilized in node/edge
definitions.

## Custom Node/Edge Definitions

A node/edge definition describes how nodes/edges are acquired from a dataset.
Each node/edge has essential attributes that make it a valid graph component,
and a definition specifies how these values are acquired or computed. Each
attribute has an expression that describes the chain of actions to acquire the
value from the dataset. An expression can be as simple as a field access or a
complex chain of transformations. Here's a simple example:

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

In plain language, this definition scans through the `targets` dataset and
generates a node for each row. The node's ID is assigned from the `id` field,
its label is set to the literal value `ensembl`, and its properties include a
single property where the key is the name of the referenced field
`approvedSymbol` and the value comes from that field.

Expressions can be chained together:

```python
expression = NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldEvidenceDiseaseId)))
```

This is equivalent to:

```python
value = normalise_curie(str(data[FieldEvidenceDiseaseId]))
```

In fact, this is almost exactly how a function will be built and run during
acquisition.

An edge definition is similar but includes two additional attributes, `source`
and `target`, to link two nodes together.

For minor customization, you can derive from one of our presets as follows:

```python
from open_targets.data.schema import FieldTargetsApprovedSymbol
from open_targets.definition import node_target
from dataclasses import replace
node_definition = replace(node_target, primary_id=FieldTargetsApprovedSymbol)
```

## Code Generation

This repository uses code generation (powered by
[jinja](https://jinja.palletsprojects.com/en/stable/)) to generate scripts such
as the Open Targets data schema represented in Python classes. The code
generation scripts are located under `code_generation`. `*.jinja` files are
templates for the generated scripts, and each template has its corresponding
script generated in the same directory.

## Future Plans
- Implement cloud streaming to eliminate the need for local dataset storage
- Develop a codeless mode for defining node/edge definitions in JSON/YAML files
- Support Open Targets metadata migration to Croissant ML
- Extend beyond Open Targets data to support various tabular data formats
- Create a comprehensive set of scientifically meaningful node/edge definitions and knowledge graph schemas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or create
an Issue if you discover any problems.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.
