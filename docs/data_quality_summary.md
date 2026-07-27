# Data Quality Summary

## Key Caveats

The dataset is suitable for product growth analytics, but these caveats should stay visible in the final project:

| Issue | Why it matters | Handling |
| --- | --- | --- |
| No explicit `event_id` | Duplicate-looking rows cannot be confidently deleted. | Create a surrogate event key and keep duplicate flags. |
| `category_code` missing in about 32% of rows | Category analysis can be biased if unknown categories are dropped. | Preserve `unknown` category labels. |
| `brand` missing in about 14% of rows | Brand analysis can be biased toward well-labeled products. | Preserve `unknown` brand labels. |
| 939 sessions map to multiple users | Session funnels can be slightly biased. | Flag multi-user sessions. |
| Product attribute conflicts exist | Product-category-brand dimensions need deterministic rules. | Use dominant observed mapping and preserve conflict flags. |
| November 15-17 purchase/revenue anomaly | Daily purchase and revenue trends may be distorted. | Annotate or exclude from sensitive daily trend interpretation. |
| Only two months of data | True churn and true LTV cannot be measured. | Use churn and customer value proxies with caveats. |

