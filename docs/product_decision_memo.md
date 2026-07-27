# Product Decision Memo

## Recommendation

Prioritize product discovery and product detail page improvements before checkout optimization.

The strongest opportunity is moving more users from product views to cart. Once users reach cart, purchase intent is already relatively strong, so checkout and cart reminders are useful but secondary.

## Business Question

How healthy is the marketplace product, and what should the Product team improve next?

## Evidence

The marketplace has meaningful scale and improving usage. Across October and November 2019, the dataset contains 109.95M events, 5.32M users, 23.02M sessions, and 206.88K products.

Usage increased month over month. Average DAU rose from 208.8K in October to 287.4K in November. MAU rose from 3.02M to 3.70M. DAU/MAU stickiness improved from 6.91% to 7.78%, which suggests improving engagement but still an occasional-use marketplace pattern.

The funnel shows that the largest loss happens before cart:

- Viewers: 5,316,128
- Cart users: 1,054,133
- Purchasers: 697,470
- View to cart rate: 19.83%
- Cart to purchase rate: 66.17%

Revenue is substantial but concentrated. Total purchase revenue was 505.15M across 1.66M purchase events. AOV was 304.35 and revenue per buyer was 724.26. Only 50,507 buyers generated 50% of total revenue, out of 697,470 total buyers.

Retention shows a real repeat-buyer base but room to improve. Repeat purchase rate was 29.99% among buyers. Repeat buyers generated much higher value than one-time buyers.

## Product Interpretation

The product is acquiring and engaging users, but many users browse without taking the next intent step. This points to a discovery and product consideration problem more than a checkout problem.

Likely product questions:

- Are users seeing relevant products quickly enough?
- Are product detail pages giving enough confidence to add to cart?
- Are category and brand experiences helping users compare alternatives?
- Are recommendations helping users move from passive browsing to active consideration?

## Recommended Product Work

1. Improve product discovery

Focus on search relevance, category navigation, recommendation modules, and ranking quality. The goal is to increase view to cart conversion.

2. Improve product detail pages

Strengthen information that helps users decide: price clarity, brand visibility, category context, product trust signals, and related items.

3. Build first-time buyer retention loops

Because repeat purchasers are much more valuable, create post-purchase recommendations, replenishment nudges, and personalized category follow-ups for first-time buyers.

4. Improve data quality for merchandising analysis

Unknown category and brand rows reduce the ability to diagnose category-level drop-off. Better taxonomy coverage would make future product recommendations more precise.

## Proposed Experiment

Test a product discovery improvement for users who view products but have not yet added to cart.

Hypothesis: improving product relevance and comparison cues will increase view to cart conversion without reducing purchase quality.

Primary metric:

- View to cart conversion rate

Secondary metrics:

- Purchase conversion rate
- Revenue per user
- AOV
- Repeat purchase rate

Guardrail metrics:

- Refund or cancellation rate, if available
- Page latency
- Session exits after product view
- Revenue concentration by top buyers

Experiment design:

- Randomize at user level
- Hold out a control group
- Run for at least one full weekly cycle
- Avoid interpreting November 15 to 17 spike behavior as normal baseline behavior

## Caveats

This analysis uses two months of behavioral data. Customer lifetime value is therefore a proxy, not true LTV. The analysis does not include margin, acquisition cost, refunds, discounts, or long-term customer history.

Feature adoption analysis is correlational. Cart usage and broader browsing are associated with stronger revenue outcomes, but the historical data alone does not prove that causing those behaviors will increase revenue. That is why the next step should be an A/B test.

## Final Decision

The Product team should first invest in product discovery and product detail page improvements, then measure impact with a user-level A/B test. Retention programs for first-time buyers should be the second priority because repeat buyers are materially more valuable than one-time buyers.
