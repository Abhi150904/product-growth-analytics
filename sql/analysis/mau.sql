-- Monthly Active Users
-- Business question: How many users engage with the product each month?

SELECT
    event_month,
    active_users AS mau
FROM analytics.mart_monthly_growth_metrics
ORDER BY 1;
