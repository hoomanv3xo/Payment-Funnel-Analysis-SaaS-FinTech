# Payment-Funnel-Analysis-SaaS-FinTech

## Executive Summary:
Fewer customers are completing their orders than we'd like to see, and we set out to find out why. I tracked every order from the moment a customer starts checkout to the moment they finish, and found that most of the lost revenue isn't happening where we expected — it's not customers giving up while entering payment details. It's happening after payment goes through, when a large share of orders never get marked as complete. I Recommend these few adjustments:
1. Fix the "payment succeeded but order didn't finish" issue first — this looks like a technical bug, not a customer experience problem, and it's currently our biggest revenue leak.
2. Look into failed or stuck payments — declined cards, timeouts, and fraud checks are causing a second significant drop.
3. Hold off on rewriting the checkout screens — that step is actually working fine, so this effort is better spent elsewhere.
4. Handle customer cancelations as a separate project — customers are canceling because they don't find the product useful, not because of price, so retention efforts should focus on onboarding. rather than discounts
   
## Business Problem:
Completed orders are directly tied to revenue for this Business. Product and sales stakeholders noticed a lower-than-expected conversion rate (users who start an order vs. users who complete it). This project identifies **where** in the workflow users fall out and **which fixes** would recover the most revenue.

![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/data%20model.png)
![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/payment%20funnel%20stages.png)

## Methodology:
1. **EDA**
2. **SQL** — extracts, cleans, and transforms raw order/payment/customer data into a funnel-ready fact table.
3. **Python** — builds the stage-by-stage funnel, visualizes drop-off, and runs a Monte Carlo simulation estimating the revenue impact of improving conversion at each step.
4. **Dashboard** — an HTML dashboard (no Power BI required) presenting the funnel, drop-off, revenue-at-risk, and cancelation reasons in one view.

   
## Skills:
1. SQL: CTEs, CASE, Union, View creation
2. Data Visualization
3. Data Wrangling
4. Data Cleaning
5. Data Science Notebook
6. Snowflake Data warehouse
7. Python

## Results and Business Recommendations:
1. **Pattern held consistently across the dataset: ** overall conversion lands around 33–35% in every version.

2. **Data suggested:**
- Sample & synthetic data pointed to **PaymentWidgetOpened→Entered** as the top leak (~33% drop) — this turned out to be a healthier step in the real data (only ~20% drop).
- The **real** top leaks are **PaymentSubmitted→Success (27% drop)** and **PaymentSuccess→Complete (37% drop)** — the latter is especially notable because payment already succeeded at that point, pointing to a technical/confirmation bug (webhook, status-sync, or redirect failure) rather than a user-hesitation problem.

![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/dropoff_chart_live.png)
![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/funnel_chart_live.png)

## Next Steps:
1. **Investigate Submitted→Success as a payments-ops issue** — card declines, gateway timeouts, fraud/3DS check failures.
2. **Investigate Success→Complete as an engineering bug**, not a UX fix — payment succeeded but the order isn't finalizing.
3. **Deprioritize payment-entry-form copy changes** — that step is healthy in the real data, despite looking like the top issue in the smaller sample.
4. **Treat post-purchase churn as a separate workstream** from the order funnel — "not useful" outranks "expensive" as a cancelation reason, suggesting an onboarding/activation problem rather than a pricing one.
