# AGENT.md

This document provides guidance for AI agents working with the Open Targets BioCypher adapter codebase.

## Project Overview

This is a **BioCypher adapter** for Open Targets data that converts Open Targets platform data into BioCypher-compatible knowledge graphs. The adapter uses a declarative, expression-based system to define how nodes and edges are extracted from Open Targets datasets. **Important**: The adapter always targets a single version of Open Targets data at a time.

## Key Concepts

### Architecture

1. **Adapter Layer** (`open_targets/adapter/`):
   - `AcquisitionContext`: Main context that manages node/edge definitions and data acquisition
   - `Expression`: Chainable expressions for data transformation
   - `ScanOperation`: Operations for scanning datasets (e.g., `RowScanOperation`)
   - `AcquisitionDefinition`: Defines how to acquire nodes/edges from datasets

2. **Definition Layer** (`open_targets/definition/`):
   - Predefined node and edge definitions (presets)
   - Located in `reference_kg/` subdirectory
   - Each definition specifies how to extract graph entities from Open Targets datasets

3. **Data Schema** (`open_targets/data/`):
   - Python classes representing Open Targets data schema
   - All dataset classes prefixed with `Dataset` (e.g., `DatasetTarget`)
   - All field classes prefixed with `Field` (e.g., `FieldTargetId`)
   - Generated via code generation (see Code Generation section)

4. **Code Generation** (`code_generation/`):
   - Uses Jinja templates to generate schema classes
   - Templates in `*.jinja` files, generated code in corresponding `*.py` files

## Important Patterns

### Node/Edge Definition Pattern

Node and edge definitions use an expression-based declarative syntax:

```python
definition = ExpressionNodeAcquisitionDefinition(
    scan_operation=RowScanOperation(dataset=DatasetTarget),
    primary_id=FieldTargetId,
    label="TARGET",
    properties=[
        (FieldTargetApprovedSymbol.name, FieldExpression(FieldTargetApprovedSymbol)),
    ],
)
```

### Expression Chaining

Expressions can be chained for complex transformations:

```python
expression = NormaliseCurieExpression(ToStringExpression(FieldExpression(FieldDiseaseId)))
```

This is equivalent to: `normalise_curie(str(data[FieldDiseaseId]))`

### Data Access Pattern

- Datasets are accessed via DuckDB for efficient processing
- Data is streamed to minimize memory usage
- Use `AcquisitionContext.get_acquisition_generator()` to get generators that yield nodes/edges

## File Structure Conventions

- **Schema classes**: `open_targets/data/schema.py` (generated)
- **Node definitions**: `open_targets/definition/reference_kg/node/`
- **Edge definitions**: `open_targets/definition/reference_kg/edge/`
- **Custom expressions**: `open_targets/definition/reference_kg/expression/`
- **Configuration**: `example/` directories (e.g. `example/full_graph/biocypher_config.yaml`)
- **Data files**: Data directories containing Open Targets parquet files (not included in repository)

## Data Versioning

**Important**: The adapter always targets a single version of Open Targets data at a time. The repository may contain data files from multiple versions, but the adapter is configured to work with one specific version.

When working with data:
- Check which version the adapter is configured for in the schema and definitions
- Ensure the `datasets_location` parameter points to data from the correct version
- The data schema classes are generated for a specific Open Targets version
- All node/edge definitions are written for a specific schema version

## Code Generation Workflow

1. **Schema Generation**: 
   - Templates: `open_targets/**/*.jinja`
   - Generated: `open_targets/data/schema.py`
   - Run: `uv run python code_generation/generate.py`

2. **When to Regenerate**:
   - When Open Targets schema changes
   - When new datasets are added
   - When field structures are updated

3. **Template Pattern**:
   - Each `.jinja` file has a corresponding generated `.py` file
   - Never edit generated files directly
   - Always edit templates and regenerate

## Common Tasks

### Adding a New Node Definition

1. Create a new file in `open_targets/definition/reference_kg/node/`
2. Define using `ExpressionNodeAcquisitionDefinition`
3. Import and add to `reference_kg_definition.node_definitions` in `kg.py`
4. For optional list-valued properties, use
   `get_null_if_empty_list_expression()` so empty lists are written as null;
   Neo4j's parquet importer otherwise stores them as byte arrays.

### Adding a New Edge Definition

1. Create a new file in `open_targets/definition/reference_kg/edge/`
2. Define using `ExpressionEdgeAcquisitionDefinition` with `source` and `target` attributes
3. Import and add to `reference_kg_definition.edge_definitions` in `kg.py`

### Creating Custom Expressions

1. Create a new file in `open_targets/definition/reference_kg/expression/`
2. Inherit from base expression classes in `open_targets/adapter/expression.py`
3. Implement the transformation logic

### Modifying Data Schema

1. **Never edit generated schema files directly**
2. Update the Jinja template in `open_targets/**/*.jinja`
3. Run code generation: `uv run python code_generation/generate.py`
4. Verify the generated schema matches expectations

## Testing

- Test files in `test/` directory
- Use pytest for running tests
- Test fixtures in `test/fixture/`
- Mock data in `test/fixture/mock/`

## Code Style

- **Python version**: 3.10 (strictly, see `pyproject.toml`)
- **Line length**: 120 characters
- **Linter**: Ruff with strict settings
- **Type checking**: Pyright in strict mode for main code
- **Docstrings**: Google convention
- **Dependencies**: Managed via `uv` (not pip)

## Important Dependencies

- `biocypher[bigdata,neo4j]>=0.12.5`: Core BioCypher framework and Neo4j support
- `duckdb>=1.4.4`: Database for efficient data processing
- `bioregistry>=0.13.21`: CURIE normalization
- `xxhash>=3.6.0,<4`: Hashing for stable identifiers
- `jinja2>=3.1.6`: Development dependency for code generation templates

## Running the Adapter

Main entry point: `example/full_graph/full_graph.py` (and other examples)

```bash
uv run python example/full_graph/full_graph.py
```

For the full graph, the parallel builder is usually faster:

```bash
uv run python example/full_graph_parallel/full_graph_parallel.py
```

Examples use the public S3 repository by default. See `example/README.md` for
local data preparation and parallel-build merge details.

This script:
1. Initializes BioCypher with config from `biocypher_config.yaml`
2. Creates an `AcquisitionContext` with node/edge definitions
3. Streams nodes and edges to BioCypher
4. Generates the knowledge graph

## Data Location Configuration

The `datasets_location` parameter in `AcquisitionContext` is required and
accepts:

- A local directory path
- A `file://` URL pointing to a local directory
- An `s3://` repository root, streamed anonymously with DuckDB

For example:

```python
from open_targets.config import DATA_REPOSITORY_URLS_S3

context = AcquisitionContext(
    node_definitions=...,
    edge_definitions=...,
    datasets_location=DATA_REPOSITORY_URLS_S3,
)
```

The S3 URL is generated from `pyproject.toml` as `DATA_REPOSITORY_URLS_S3`.
Remote access requires the `httpfs` DuckDB extension, which is installed and
loaded automatically.

## Common Pitfalls

1. **Don't edit generated files**: Always edit templates and regenerate
2. **Version mismatch**: The adapter targets a single data version. Ensure the data directory, schema, and definitions all match the same Open Targets version
3. **Expression order matters**: Chain expressions in the correct order
4. **Field references**: Always use schema classes (e.g., `FieldTargetId`) not string literals
5. **Optional list properties**: Neo4j's parquet importer stores empty lists as
   `b''` with type `LIST<INTEGER>`. Use
   `get_null_if_empty_list_expression()` for optional list-valued node
   properties, or otherwise return `None` instead of `[]`.
6. **Component success reporting**: BioCypher can log `ERROR` while the
   component still reports `OK`. Check component `console.log` files and verify
   expected output files and counts; `parallel_errors.log` only records process
   failures.
7. **Memory usage**: The adapter streams data, but very large datasets may still require attention

## Debugging Tips

1. Check `biocypher-log/` for BioCypher execution logs
2. For parallel builds, inspect the merged `console.log` for `ERROR` lines and
   verify that every expected component produced an output file
3. Use `limit` parameter in `AcquisitionContext` to test with small datasets
4. Verify dataset paths and structure match expected format
5. Check that all required datasets are present in the data directory

## Future Development Areas

- Codeless JSON/YAML definition mode
- Extended tabular data format support
- Additional cloud storage backends

## Key Files to Understand

1. `open_targets/adapter/context.py` - Main acquisition context
2. `open_targets/adapter/expression.py` - Expression system
3. `open_targets/definition/reference_kg/kg.py` - Main KG definition
4. `open_targets/definition/helper.py` - Shared expression helpers
5. `example/full_graph/full_graph.py` - Execution script example
6. `example/full_graph_parallel/full_graph_parallel.py` - Parallel build entry point
7. `code_generation/generate.py` - Code generation logic

## When Making Changes

1. **Schema changes**: Update templates → regenerate → update definitions
2. **Definition changes**: Update definition files → test with small dataset
3. **New features**: Follow existing patterns in adapter layer
4. **Bug fixes**: Check expression chains and data access patterns first

