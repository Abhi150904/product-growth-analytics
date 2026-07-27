-- Product Funnel
-- Business question: Where do users drop from view to cart to purchase?

SELECT
    COUNT(CASE WHEN view_events > 0 THEN 1 END) AS viewers,
    COUNT(CASE WHEN cart_events > 0 THEN 1 END) AS cart_users,
    COUNT(CASE WHEN purchase_events > 0 THEN 1 END) AS purchasers,
    COUNT(CASE WHEN cart_events > 0 THEN 1 END) * 1.0
        / NULLIF(COUNT(CASE WHEN view_events > 0 THEN 1 END), 0) AS view_to_cart_rate,
    COUNT(CASE WHEN purchase_events > 0 THEN 1 END) * 1.0
        / NULLIF(COUNT(CASE WHEN cart_events > 0 THEN 1 END), 0) AS cart_to_purchase_rate
FROM analytics.mart_user_lifecycle;
