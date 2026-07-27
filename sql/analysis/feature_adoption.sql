-- Feature Adoption
-- Business question: Which product behaviors do users adopt?

SELECT
    event_type AS feature,
    events,
    users AS adopting_users,
    sessions AS adopting_sessions
FROM analytics.event_type_summary
ORDER BY adopting_users DESC;
