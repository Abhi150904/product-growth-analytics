from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from product_growth_analytics.config import PROCESSED_DATA_DIR, SQL_DIR


DATABASE_PATH = PROCESSED_DATA_DIR / "product_growth.duckdb"


def connect() -> duckdb.DuckDBPyConnection:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            "Missing processed DuckDB database. Run "
            "`python scripts/01_build_transformation_pipeline.py` first."
        )
    return duckdb.connect(str(DATABASE_PATH), read_only=True)


def read_sql(relative_path: str) -> str:
    path = SQL_DIR / relative_path
    return path.read_text(encoding="utf-8")


def query_df(con: duckdb.DuckDBPyConnection, sql: str) -> pd.DataFrame:
    return con.execute(sql).fetchdf()
