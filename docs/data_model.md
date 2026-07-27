# Analytical Data Model

## Model Purpose

The model turns raw event logs into reusable Product Analytics tables for growth metrics, funnels, retention, revenue, customer value, and feature adoption.

## Compact Model

This project uses an aggregate-first model so the notebooks and dashboard stay fast on a very large source dataset.

| Object | Grain | Purpose |
| --- | --- |
| `analytics.dataset_overview` | One row | Dataset coverage and date range. |
| `analytics.event_type_summary` | One row per event type | Event mix and feature adoption. |
| `analytics.data_quality_summary` | One row | Key caveats and quality flags. |
| `analytics.mart_daily_growth_metrics` | One row per date | DAU, daily funnel signals, purchases, and revenue. |
| `analytics.mart_weekly_growth_metrics` | One row per week | WAU, weekly purchases, and revenue. |
| `analytics.mart_monthly_growth_metrics` | One row per month | MAU, monthly purchases, and revenue. |
| `analytics.mart_weekly_user_activity` | One row per user-week | Retention cohort analysis. |
| `analytics.mart_user_lifecycle` | One row per user | Lifecycle stage, repeat purchase, customer value proxy, feature adoption. |
| `analytics.mart_product_funnel` | One row per product | Product/category funnel and revenue analysis. |
| `analytics.fact_purchases` | One row per purchase event | Revenue, AOV, ARPU, customer value, and purchase cohorts. |

## Key Rules

- Revenue comes only from `purchase` events.
- Missing category and brand values are kept as `unknown`.
- The full event-level fact is not materialized by default because the source has about 110M rows.
- November 15-17 is flagged as a purchase/revenue anomaly window.
