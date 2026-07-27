-- Weekly Retention
-- Business question: Do users come back after their first observed week?

WITH first_seen AS (
    SELECT
        user_id,
        DATE_TRUNC('week', first_seen_date) AS cohort_week
    FROM analytics.mart_user_lifecycle
),
cohort_size AS (
    SELECT
        cohort_week,
        COUNT(DISTINCT user_id) AS cohort_users
    FROM first_seen
    GROUP BY 1
),
weekly_activity AS (
    SELECT
        user_id,
        event_week AS active_week
    FROM analytics.mart_weekly_user_activity
)
SELECT
    first_seen.cohort_week,
    DATE_DIFF('week', first_seen.cohort_week, weekly_activity.active_week) AS week_number,
    COUNT(DISTINCT weekly_activity.user_id) AS retained_users,
    cohort_size.cohort_users,
    COUNT(DISTINCT weekly_activity.user_id) * 1.0
        / NULLIF(cohort_size.cohort_users, 0) AS retention_rate
FROM first_seen
JOIN weekly_activity
    ON first_seen.user_id = weekly_activity.user_id
   AND weekly_activity.active_week >= first_seen.cohort_week
JOIN cohort_size
    ON first_seen.cohort_week = cohort_size.cohort_week
GROUP BY 1, 2, 4
ORDER BY 1, 2;
