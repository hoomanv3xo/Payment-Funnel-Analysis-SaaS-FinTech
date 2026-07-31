# Payment-Funnel-Analysis-SaaS-FinTech

## Executive Summary:
Analysis of where users drop out of the order/subscription workflow between opening the payment widget and completing an order, with SQL extraction, Python funnel modeling + revenue simulation, and
an HTML dashboard.

## Business Problem:
Completed orders are directly tied to revenue for this Business. Product and sales stakeholders noticed a lower-than-expected conversion rate (users who start an order vs. users who complete it). This project identifies **where** in the workflow users fall out and **which fixes** would recover the most revenue.

![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/data%20model.png)
![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/payment%20funnel%20stages.png)

## Methodology:
1. EDA
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

2. **Synthetic data suggested:**
- Sample & synthetic data pointed to **PaymentWidgetOpened→Entered** as the top leak (~33% drop) — this turned out to be a healthier step in the real data (only ~20% drop).
- The **real** top leaks are **PaymentSubmitted→Success (27% drop)** and **PaymentSuccess→Complete (37% drop)** — the latter is especially notable because payment already succeeded at that point, pointing to a technical/confirmation bug (webhook, status-sync, or redirect failure) rather than a user-hesitation problem.

![Data Model]()
![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/image2.png)
![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/image3.png)

## Next Steps:
1. **Investigate Submitted→Success as a payments-ops issue** — card declines, gateway timeouts, fraud/3DS check failures.
2. **Investigate Success→Complete as an engineering bug**, not a UX fix — payment succeeded but the order isn't finalizing.
3. **Deprioritize payment-entry-form copy changes** — that step is healthy in the real data, despite looking like the top issue in the smaller sample.
4. **Treat post-purchase churn as a separate workstream** from the order funnel — "not useful" outranks "expensive" as a cancelation reason, suggesting an onboarding/activation problem rather than a pricing one.
