-- Customer Cohorts
-- Business question: When did users first enter the product, and how do cohorts behave later?

SELECT
    user_id,
    DATE_TRUNC('week', first_seen_date) AS cohort_week
FROM analytics.mart_user_lifecycle;
