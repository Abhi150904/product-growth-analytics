-- Weekly Active Users
-- Business question: How many users engage with the product each week?

SELECT
    event_week,
    active_users AS wau
FROM analytics.mart_weekly_growth_metrics
ORDER BY 1;
