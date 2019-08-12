# Testing Data and Utilities for Apache Parquet

## Difficult datasets

Some datasets are included which are tricky to handle:

| dataset name | comments |
|---|---|
| `double_1Grows_1kgroups.parquet` | A single column of repeated `0.0`. There are `2^30` total rows divided between `2^10` row groups. This is useful for testing incremental scanning and materialization; naive load (using `pyarrow.parquet.read_table`) of this file yields a memory footprint of 25GB on my machine |
