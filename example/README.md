# Examples

This directory contains runnable examples demonstrating how to use the Open Targets BioCypher adapter.

## Available Examples

### Full Graph (`full_graph/`)

Builds the complete reference knowledge graph using all predefined node and edge definitions.

**Run:**
```bash
uv run python example/full_graph/full_graph.py
```

**Data:** Uses the public S3 repository by default. For local data, see [Local Data Preparation](#local-data-preparation).

### Custom Subset (`custom_subset/`)

Demonstrates how to build a knowledge graph with a custom selection of node and edge definitions.

**Run:**
```bash
uv run python example/custom_subset/custom_subset.py
```

**Data:** Uses the public S3 repository by default. For local data, see [Local Data Preparation](#local-data-preparation).

### Parallel Full Graph (`full_graph_parallel/`)

Builds the full reference graph in parallel by grouping node/edge definitions by
label. Each label is one component with its own BioCypher output directory, and
components run through a bounded process pool.

**Run:**
```bash
uv run python example/full_graph_parallel/full_graph_parallel.py
```

**Data:** Uses the public S3 repository by default. For local data, see
[Local Data Preparation](#local-data-preparation). Components run with a fixed
concurrency of 32 processes; failures are recorded in `parallel_errors.log` and
the run continues.

At the end, successful component outputs are moved into a `merged/`
subdirectory containing flat parquet files, a merged `schema_info.yaml`, a
single combined Neo4j import script, and a combined `console.log`. The
per-component directories are removed after merging. Set `MERGE_RESULTS = False`
in `full_graph_parallel.py` to skip merging and keep the component directories.

The console falls back automatically in Jupyter/IDLE or when fd redirection is
unavailable. Set `FORCE_STREAM_CAPTURE = True` in `console.py` to force it.

## Local Data Preparation

The examples use the public S3 repository by default. To use local data instead:

1. Download the Open Targets 25.12 output from the
   [Open Targets FTP server](https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.12/output/).
2. Create a `datasets` directory in the project root, or use any other path.
3. Place each dataset in a directory named after its dataset ID. The adapter
   reads parquet files from
   `<datasets_location>/<dataset.id>/**/*.parquet`.

```text
datasets/
├── target/
│   └── *.parquet
├── disease/
│   └── *.parquet
├── drug_molecule/
│   └── *.parquet
├── association_overall_direct/
│   └── *.parquet
├── drug_indication/
│   └── *.parquet
└── ...
```

Use `datasets_location="datasets"` in the example, or a `file://` URL. The full
graph requires all datasets used by the reference definitions. The custom subset
requires only:

- `target`
- `disease`
- `drug_molecule`
- `association_overall_direct`
- `drug_indication`

## Creating Your Own Example

1. Create a new directory under `example/`
2. Copy `biocypher_config.yaml` and `schema_config.yaml` from an existing example
3. Create your Python script importing definitions from `open_targets.definition.reference_kg`
4. See [Local Data Preparation](#local-data-preparation) for the expected dataset layout
5. See existing examples for the pattern

