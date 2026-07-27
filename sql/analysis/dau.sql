-- Daily Active Users
-- Business question: How many users engage with the product each day?

SELECT
    event_date,
    active_users AS dau
FROM analytics.mart_daily_growth_metrics
ORDER BY 1;
