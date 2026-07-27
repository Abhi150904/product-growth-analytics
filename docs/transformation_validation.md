# Transformation Validation

## Pipeline Status

Validation status: **passed**

Local DuckDB database:

```text
C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\product_growth.duckdb
```

## Materialized Tables

| Table | Rows |
| --- | --- |
| dataset_overview | 1 |
| event_type_summary | 3 |
| data_quality_summary | 1 |
| mart_daily_growth_metrics | 61 |
| mart_weekly_growth_metrics | 9 |
| mart_weekly_user_activity | 10,519,486 |
| mart_monthly_growth_metrics | 2 |
| mart_user_lifecycle | 5,316,649 |
| mart_product_funnel | 206,876 |
| fact_purchases | 1,659,788 |

## Validation Checks

| Check | Severity | Status |
| --- | --- | --- |
| overview has events | high | pass |
| event types are expected | high | pass |
| daily revenue reconciles to purchases | high | pass |
| user lifecycle has unique users | high | pass |
| product funnel has unique products | medium | pass |
| purchase revenue is non-negative | high | pass |

## Exported Power BI Marts

| File | Local path |
| --- | --- |
| dataset_overview.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\dataset_overview.parquet |
| event_type_summary.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\event_type_summary.parquet |
| data_quality_summary.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\data_quality_summary.parquet |
| mart_daily_growth_metrics.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_daily_growth_metrics.parquet |
| mart_weekly_growth_metrics.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_weekly_growth_metrics.parquet |
| mart_weekly_user_activity.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_weekly_user_activity.parquet |
| mart_monthly_growth_metrics.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_monthly_growth_metrics.parquet |
| mart_user_lifecycle.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_user_lifecycle.parquet |
| mart_product_funnel.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\mart_product_funnel.parquet |
| fact_purchases.parquet | C:\Users\Abhinav Sinha\Documents\product-growth-analytics\data\processed\powerbi_marts\fact_purchases.parquet |

## Notes

- Generated data files are intentionally ignored by Git.
- `fact_events` preserves duplicate-looking raw records with `duplicate_sequence` and `is_duplicate_signature`.
- `mart_daily_growth_metrics` flags the November 15-17 purchase anomaly window.
- Power BI should connect to the exported Parquet files in `data/processed/powerbi_marts/`.
