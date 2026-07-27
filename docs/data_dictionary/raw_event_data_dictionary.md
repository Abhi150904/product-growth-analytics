# Phase 1 Data Dictionary

## Raw Event Table Columns

| Column | DuckDB type | Business meaning | Max null rate by file | Max approx distinct by file |
| --- | --- | --- | --- | --- |
| event_time | TIMESTAMP | Timestamp of the user event. | 0.00% | 2,675,444 |
| event_type | VARCHAR | User action, such as view, cart, remove_from_cart, or purchase. | 0.00% | 3 |
| product_id | BIGINT | Product identifier attached to the event. | 0.00% | 219,168 |
| category_id | BIGINT | Numeric category identifier attached to the product/event. | 0.00% | 872 |
| category_code | VARCHAR | Hierarchical category label when available. | 32.44% | 122 |
| brand | VARCHAR | Product brand when available. | 14.40% | 4,037 |
| price | DOUBLE | Product price recorded on the event. | 0.00% | 78,322 |
| user_id | BIGINT | User identifier. | 0.00% | 3,902,584 |
| user_session | VARCHAR | Session identifier grouping user events. | 0.00% | 15,889,294 |

## Table Purpose

The raw monthly CSV files are append-only event logs. They are the source for future analytical marts:

- Customer dimension from `user_id`
- Session dimension from `user_session`
- Product dimension from `product_id`, `category_id`, `category_code`, and `brand`
- Event fact from all event rows
- Purchase and revenue facts from purchase events

## Notes For Future Phases

- `category_code` and `brand` may be incomplete, so category and brand analyses need explicit coverage checks.
- `price` is event-level price, not necessarily order-level revenue unless the event is a purchase.
- `user_session` is useful for funnel analysis, but session quality must be validated before we rely on it.
