# BioCypher Open Targets Data (25.12) Adapter

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

This repository contains a [BioCypher](https://biocypher.org) adapter for Open
Targets data version 25.12. The project is currently under active development.

> **AI Usage Disclaimer**: This project makes extensive use of AI. The author guarantees that every effort has been made to oversee the architecture and coding style and review the generated content for quality and consistency.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Reference Knowledge Graph](#reference-knowledge-graph)
- [Open Targets Data Schema](#open-targets-data-schema)
- [Code Generation](#code-generation)
- [Contributing](#contributing)
- [License](#license)

## Overview

BioCypher's modular design enables the use of different adapters to consume
various data sources and produce knowledge graphs. This adapter serves as a
["secondary
adapter"](https://biocypher.org/latest/learn/tutorials/tutorial003_adapters/)
for [Open Targets data](https://platform.opentargets.org/downloads), meaning it
adapts a pre-harmonised composite of atomic resources via the Open Targets
pipeline.

The adapter includes a comprehensive reference knowledge graph with predefined
sets of node types (entities) and edge types (relationships), or in the language
of this adapter, presets of node and edge `definitions`. A script is provided
to run BioCypher with the adapter, creating a knowledge graph with all predefined
nodes and edges. On a consumer laptop, building the full graph typically takes
1-2 hours.

**Key Features:**
- **Includes a comprehensive knowledge graph definition designed to cover all data provided by the Open Targets Platform.** See [Reference Knowledge Graph](#reference-knowledge-graph) for details.
- Declarative syntax for graph schema construction
- Powered by [duckdb](https://duckdb.org/) for fast and memory-efficient processing
- True streaming from datasets to BioCypher with minimal intermediate memory usage
- Type-safe schema representation with Python classes

## Prerequisites

- [uv](https://github.com/astral-sh/uv) for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/biocypher/open-targets.git
   cd open-targets
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Activate the virtual environment (optional):
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   .venv\Scripts\activate    # On Windows
   ```
   
   Or run commands directly with `uv run`:
   ```bash
   uv run python <script>
   ```

## Usage

Runnable examples are provided in the `example/` directory. Each example includes:
- A Python script demonstrating usage
- Configuration files
- Local data preparation instructions in `example/README.md`

> [!IMPORTANT]
> When running the example scripts, ensure your current working directory is the project root.


### Quick Start

1. Follow the [Installation](#installation) steps
2. Examples use the public S3 repository by default. For local data, follow the
   [Local Data Preparation](example/README.md#local-data-preparation) guide.
3. **Important:** Run example scripts from the project root:
   ```bash
   uv run python example/full_graph/full_graph.py
   ```

### Available Examples

- **Full Graph** (`example/full_graph/`): Builds the complete reference knowledge graph using all predefined definitions
- **Custom Subset** (`example/custom_subset/`): Demonstrates selecting specific node/edge definitions
- **Parallel Full Graph** (`example/full_graph_parallel/`): Builds the full reference graph in parallel, grouping definitions by label

See `example/README.md` for details on all available examples and how to create your own.

### Data Sources

`AcquisitionContext` accepts local and remote data through the same
`datasets_location` parameter:

```python
from open_targets.adapter.context import AcquisitionContext
from open_targets.config import DATA_REPOSITORY_URLS_S3

# Local directory
context = AcquisitionContext(
    node_definitions=...,
    edge_definitions=...,
    datasets_location="datasets",
)

# Public S3 bucket, streamed anonymously with DuckDB
context = AcquisitionContext(
    node_definitions=...,
    edge_definitions=...,
    datasets_location=DATA_REPOSITORY_URLS_S3,
)
```

Only local locations and `s3://` URLs are supported.

## Reference Knowledge Graph

The reference knowledge graph includes 40+ node types and 50+ edge types. **Each definition file contains detailed docstrings explaining what it does, what data it uses, and how it works.**

### Finding Definition Files

- **Node definitions**: `open_targets/definition/reference_kg/node/`
- **Edge definitions**: `open_targets/definition/reference_kg/edge/`
- **Complete list**: `open_targets/definition/reference_kg/kg.py`

### Reading Docstrings

Each definition file (e.g., `node_target.py`, `edge_molecule_has_adverse_reaction_adverse_reaction.py`) starts with a module-level docstring that describes:
- What entities/relationships the definition creates
- Which Open Targets datasets it uses
- How the data is transformed
- What properties are included

**Example:**
```python
# In open_targets/definition/reference_kg/node/node_target.py
"""Summary: Ensembl target gene nodes (symbol/name/biotype/functions).

Definition for TARGET nodes: scans the Targets parquet to emit Ensembl gene
targets with symbol, name, biotype, and function descriptions as the core
target entities used across drug, association, and annotation edges in the KG.
"""
```

To explore available definitions:
1. Browse the files in `open_targets/definition/reference_kg/node/` and `edge/`
2. Read the docstring at the top of each file
3. Check `kg.py` to see how definitions are organized

For details on creating custom definitions, see the adapter layer documentation in `open_targets/adapter/` and examine existing definitions as examples.

## Open Targets Data Schema

The full schema of Open Targets data is represented as Python classes in `open_targets/data/schema.py`. This provides type checking for dataset and field references.

**Naming Conventions:**
- Dataset classes: `Dataset` prefix (e.g., `DatasetTargets`, `DatasetDiseases`)
- Field classes: `Field` prefix (e.g., `FieldTargetsId`, `FieldTargetsApprovedSymbol`)
- Field names follow their structural location in datasets

The schema is generated from Open Targets metadata using code generation (see below). Schema classes are used throughout node/edge definitions for type-safe data access.

## Code Generation

The Open Targets data schema is generated using [Jinja](https://jinja.palletsprojects.com/en/stable/) templates.

- **Templates**: `open_targets/*.jinja`
- **Generated code**: `open_targets/data/schema.py`
- **Generation script**: `code_generation/generate.py`

**Important:** Never edit generated files directly. Always modify templates and regenerate:
```bash
python code_generation/generate.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or create
an Issue if you discover any problems.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.
