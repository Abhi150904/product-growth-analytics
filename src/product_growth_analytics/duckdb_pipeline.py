from __future__ import annotations

from pathlib import Path

import duckdb

from product_growth_analytics.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


DATASET_MARKER = RAW_DATA_DIR / "KAGGLE_DATASET_PATH.txt"
DATABASE_PATH = PROCESSED_DATA_DIR / "product_growth.duckdb"
EXPORT_DIR = PROCESSED_DATA_DIR / "powerbi_marts"


def read_dataset_path() -> Path:
    if not DATASET_MARKER.exists():
        raise FileNotFoundError(
            f"Missing {DATASET_MARKER}. Run scripts/00_download_dataset.py first."
        )
    dataset_path = Path(DATASET_MARKER.read_text(encoding="utf-8").strip())
    if not dataset_path.exists():
        raise FileNotFoundError(f"KaggleHub dataset path does not exist: {dataset_path}")
    return dataset_path


def duckdb_path(path: Path) -> str:
    return str(path).replace("\\", "/").replace("'", "''")


def connect_database() -> duckdb.DuckDBPyConnection:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DATABASE_PATH))
    con.execute("PRAGMA threads=4")
    con.execute("PRAGMA memory_limit='6GB'")
    return con


def create_raw_events_view(con: duckdb.DuckDBPyConnection, dataset_path: Path) -> None:
    csv_glob = dataset_path / "*.csv"
    con.execute(
        f"""
        CREATE OR REPLACE VIEW raw_events AS
        SELECT
            CAST(event_time AS TIMESTAMP) AS event_time,
            CAST(event_time AS DATE) AS event_date,
            DATE_TRUNC('week', CAST(event_time AS TIMESTAMP)) AS event_week,
            DATE_TRUNC('month', CAST(event_time AS TIMESTAMP)) AS event_month,
            CAST(event_type AS VARCHAR) AS event_type,
            CAST(product_id AS BIGINT) AS product_id,
            CAST(category_id AS BIGINT) AS category_id,
            COALESCE(NULLIF(TRIM(CAST(category_code AS VARCHAR)), ''), 'unknown') AS category_code,
            COALESCE(NULLIF(LOWER(TRIM(CAST(brand AS VARCHAR))), ''), 'unknown') AS brand,
            CAST(price AS DOUBLE) AS price,
            CAST(user_id AS BIGINT) AS user_id,
            CAST(user_session AS VARCHAR) AS user_session
        FROM read_csv_auto(
            '{duckdb_path(csv_glob)}',
            header=true,
            union_by_name=true
        )
        """
    )


def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("CREATE SCHEMA IF NOT EXISTS analytics")


def build_summary_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.dataset_overview AS
        SELECT
            COUNT(*) AS events,
            COUNT(DISTINCT user_id) AS users,
            COUNT(DISTINCT user_session) AS sessions,
            COUNT(DISTINCT product_id) AS products,
            COUNT(DISTINCT category_id) AS categories,
            COUNT(DISTINCT category_code) AS category_codes,
            COUNT(DISTINCT brand) AS brands,
            MIN(event_time) AS min_event_time,
            MAX(event_time) AS max_event_time
        FROM raw_events
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.event_type_summary AS
        SELECT
            event_type,
            COUNT(*) AS events,
            COUNT(DISTINCT user_id) AS users,
            COUNT(DISTINCT user_session) AS sessions
        FROM raw_events
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.data_quality_summary AS
        SELECT
            SUM(CASE WHEN category_code = 'unknown' THEN 1 ELSE 0 END) AS unknown_category_rows,
            SUM(CASE WHEN brand = 'unknown' THEN 1 ELSE 0 END) AS unknown_brand_rows,
            SUM(CASE WHEN user_session IS NULL THEN 1 ELSE 0 END) AS null_session_rows,
            SUM(CASE WHEN price < 0 THEN 1 ELSE 0 END) AS negative_price_rows,
            SUM(CASE WHEN price = 0 THEN 1 ELSE 0 END) AS zero_price_rows,
            SUM(CASE WHEN event_date BETWEEN DATE '2019-11-15' AND DATE '2019-11-17' THEN 1 ELSE 0 END) AS anomaly_window_rows
        FROM raw_events
        """
    )


def build_growth_marts(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_daily_growth_metrics AS
        SELECT
            event_date,
            COUNT(*) AS events,
            COUNT(DISTINCT user_id) AS active_users,
            COUNT(DISTINCT user_session) AS sessions,
            COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS view_events,
            COUNT(CASE WHEN event_type = 'cart' THEN 1 END) AS cart_events,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchase_events,
            COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS viewers,
            COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS cart_users,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchasing_users,
            SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue,
            event_date BETWEEN DATE '2019-11-15' AND DATE '2019-11-17' AS is_purchase_anomaly_window
        FROM raw_events
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_weekly_growth_metrics AS
        SELECT
            event_week,
            COUNT(*) AS events,
            COUNT(DISTINCT user_id) AS active_users,
            COUNT(DISTINCT user_session) AS sessions,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchase_events,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchasing_users,
            SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue
        FROM raw_events
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_weekly_user_activity AS
        SELECT DISTINCT
            user_id,
            event_week
        FROM raw_events
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_monthly_growth_metrics AS
        SELECT
            event_month,
            COUNT(*) AS events,
            COUNT(DISTINCT user_id) AS active_users,
            COUNT(DISTINCT user_session) AS sessions,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchase_events,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchasing_users,
            SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue
        FROM raw_events
        GROUP BY 1
        """
    )


def build_user_and_product_marts(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_user_lifecycle AS
        SELECT
            user_id,
            MIN(event_date) AS first_seen_date,
            MAX(event_date) AS last_seen_date,
            MIN(CASE WHEN event_type = 'purchase' THEN event_date END) AS first_purchase_date,
            COUNT(*) AS events,
            COUNT(DISTINCT user_session) AS sessions,
            COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS view_events,
            COUNT(CASE WHEN event_type = 'cart' THEN 1 END) AS cart_events,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchase_events,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN event_date END) AS purchase_days,
            COUNT(DISTINCT category_id) AS categories_engaged,
            COUNT(DISTINCT CASE WHEN brand <> 'unknown' THEN brand END) AS known_brands_engaged,
            SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue,
            CASE
                WHEN COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) >= 1
                    AND COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN event_date END) >= 2
                    THEN 'repeat_purchaser'
                WHEN COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) >= 1 THEN 'purchaser'
                WHEN COUNT(CASE WHEN event_type = 'cart' THEN 1 END) >= 1 THEN 'cart_user'
                WHEN COUNT(CASE WHEN event_type = 'view' THEN 1 END) >= 2
                    OR COUNT(DISTINCT user_session) >= 2 THEN 'engaged_browser'
                WHEN COUNT(CASE WHEN event_type = 'view' THEN 1 END) >= 1 THEN 'product_viewer'
                ELSE 'visitor'
            END AS lifecycle_stage,
            MAX(event_date) < DATE '2019-11-24' AS is_dormant_proxy
        FROM raw_events
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.mart_product_funnel AS
        SELECT
            product_id,
            MODE(category_id) AS category_id,
            MODE(category_code) AS category_code,
            MODE(brand) AS brand,
            COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS view_events,
            COUNT(CASE WHEN event_type = 'cart' THEN 1 END) AS cart_events,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchase_events,
            COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS viewing_users,
            COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS cart_users,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchasing_users,
            SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue
        FROM raw_events
        GROUP BY 1
        """
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics.fact_purchases AS
        SELECT
            event_time AS purchase_time,
            event_date AS purchase_date,
            event_week AS purchase_week,
            event_month AS purchase_month,
            user_id,
            user_session,
            product_id,
            category_id,
            category_code,
            brand,
            price AS revenue,
            event_date BETWEEN DATE '2019-11-15' AND DATE '2019-11-17' AS is_purchase_anomaly_window
        FROM raw_events
        WHERE event_type = 'purchase'
        """
    )


def export_powerbi_marts(con: duckdb.DuckDBPyConnection) -> list[Path]:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    tables = [
        "dataset_overview",
        "event_type_summary",
        "data_quality_summary",
        "mart_daily_growth_metrics",
        "mart_weekly_growth_metrics",
        "mart_weekly_user_activity",
        "mart_monthly_growth_metrics",
        "mart_user_lifecycle",
        "mart_product_funnel",
        "fact_purchases",
    ]
    exported_paths = []
    for table in tables:
        output_path = EXPORT_DIR / f"{table}.parquet"
        con.execute(
            f"""
            COPY analytics.{table}
            TO '{duckdb_path(output_path)}'
            (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )
        exported_paths.append(output_path)
    return exported_paths


def validate_pipeline(con: duckdb.DuckDBPyConnection) -> list[dict[str, object]]:
    checks = [
        {
            "check_name": "overview has events",
            "severity": "high",
            "sql": "SELECT events > 0 FROM analytics.dataset_overview",
        },
        {
            "check_name": "event types are expected",
            "severity": "high",
            "sql": """
                SELECT COUNT(*) = 0
                FROM analytics.event_type_summary
                WHERE event_type NOT IN ('view', 'cart', 'purchase')
            """,
        },
        {
            "check_name": "daily revenue reconciles to purchases",
            "severity": "high",
            "sql": """
                SELECT
                    ABS(
                        (SELECT SUM(revenue) FROM analytics.mart_daily_growth_metrics)
                        -
                        (SELECT SUM(revenue) FROM analytics.fact_purchases)
                    ) < 0.01
            """,
        },
        {
            "check_name": "user lifecycle has unique users",
            "severity": "high",
            "sql": """
                SELECT COUNT(*) = COUNT(DISTINCT user_id)
                FROM analytics.mart_user_lifecycle
            """,
        },
        {
            "check_name": "product funnel has unique products",
            "severity": "medium",
            "sql": """
                SELECT COUNT(*) = COUNT(DISTINCT product_id)
                FROM analytics.mart_product_funnel
            """,
        },
        {
            "check_name": "purchase revenue is non-negative",
            "severity": "high",
            "sql": """
                SELECT COUNT(*) = 0
                FROM analytics.fact_purchases
                WHERE revenue < 0
            """,
        },
    ]

    results = []
    for check in checks:
        passed = bool(con.execute(check["sql"]).fetchone()[0])
        results.append(
            {
                "check_name": check["check_name"],
                "severity": check["severity"],
                "status": "pass" if passed else "fail",
            }
        )
    return results


def collect_table_counts(con: duckdb.DuckDBPyConnection) -> list[dict[str, object]]:
    table_names = [
        "dataset_overview",
        "event_type_summary",
        "data_quality_summary",
        "mart_daily_growth_metrics",
        "mart_weekly_growth_metrics",
        "mart_weekly_user_activity",
        "mart_monthly_growth_metrics",
        "mart_user_lifecycle",
        "mart_product_funnel",
        "fact_purchases",
    ]
    return [
        {
            "table_name": table_name,
            "rows": con.execute(f"SELECT COUNT(*) FROM analytics.{table_name}").fetchone()[
                0
            ],
        }
        for table_name in table_names
    ]
