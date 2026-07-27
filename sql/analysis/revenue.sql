-- Revenue Metrics
-- Business question: How much revenue does the product generate, and from whom?

SELECT
    purchase_date,
    SUM(revenue) AS revenue,
    COUNT(*) AS purchase_events,
    COUNT(DISTINCT user_id) AS purchasing_users,
    SUM(revenue) * 1.0 / NULLIF(COUNT(*), 0) AS aov_per_purchase_event,
    SUM(revenue) * 1.0 / NULLIF(COUNT(DISTINCT user_id), 0) AS revenue_per_purchasing_user
FROM analytics.fact_purchases
GROUP BY 1
ORDER BY 1;
