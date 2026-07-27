from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from product_growth_analytics.duckdb_pipeline import (
    DATABASE_PATH,
    build_growth_marts,
    build_summary_tables,
    build_user_and_product_marts,
    connect_database,
    create_raw_events_view,
    create_schema,
    export_powerbi_marts,
    read_dataset_path,
    validate_pipeline,
    collect_table_counts,
)


DOCS_DIR = PROJECT_ROOT / "docs"
VALIDATION_OUTPUT = DOCS_DIR / "transformation_validation.md"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def write_validation_report(
    table_counts: list[dict[str, object]],
    validation_results: list[dict[str, object]],
    exported_paths: list[Path],
) -> None:
    table_rows = [
        [item["table_name"], f"{item['rows']:,}"] for item in table_counts
    ]
    validation_rows = [
        [item["check_name"], item["severity"], item["status"]]
        for item in validation_results
    ]
    export_rows = [[path.name, str(path)] for path in exported_paths]

    failed_checks = [
        item for item in validation_results if item["status"] != "pass"
    ]
    status = "passed" if not failed_checks else "failed"

    content = f"""# Transformation Validation

## Pipeline Status

Validation status: **{status}**

Local DuckDB database:

```text
{DATABASE_PATH}
```

## Materialized Tables

{markdown_table(["Table", "Rows"], table_rows)}

## Validation Checks

{markdown_table(["Check", "Severity", "Status"], validation_rows)}

## Exported Power BI Marts

{markdown_table(["File", "Local path"], export_rows)}

## Notes

- Generated data files are intentionally ignored by Git.
- `fact_events` preserves duplicate-looking raw records with `duplicate_sequence` and `is_duplicate_signature`.
- `mart_daily_growth_metrics` flags the November 15-17 purchase anomaly window.
- Power BI should connect to the exported Parquet files in `data/processed/powerbi_marts/`.
"""

    VALIDATION_OUTPUT.write_text(content, encoding="utf-8")


def main() -> None:
    dataset_path = read_dataset_path()
    con = connect_database()

    print(f"Dataset path: {dataset_path}")
    print(f"DuckDB database: {DATABASE_PATH}")

    print("Creating raw_events view...")
    create_raw_events_view(con, dataset_path)

    print("Creating analytics schema...")
    create_schema(con)

    print("Building compact summary tables...")
    build_summary_tables(con)

    print("Building growth marts...")
    build_growth_marts(con)

    print("Building user, product, and purchase marts...")
    build_user_and_product_marts(con)

    print("Collecting row counts...")
    table_counts = collect_table_counts(con)

    print("Running validation checks...")
    validation_results = validate_pipeline(con)

    print("Exporting Power BI marts...")
    exported_paths = export_powerbi_marts(con)

    write_validation_report(table_counts, validation_results, exported_paths)

    if any(result["status"] != "pass" for result in validation_results):
        failures = pd.DataFrame(validation_results)
        print(failures.to_string(index=False))
        raise SystemExit("Transformation validation failed.")

    print(f"Wrote {VALIDATION_OUTPUT}")
    print("Transformation pipeline completed successfully.")


if __name__ == "__main__":
    main()
