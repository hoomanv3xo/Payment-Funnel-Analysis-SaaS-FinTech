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

##    Business Recommendations:
1. Simplify the payment entry experience by adding options like Apple Pay, Google Pay, or other methods that eliminate the need to manually enter credit card details each time. This can help reduce user errors caused by incorrect payment information.

2. Connect with the third-party payment processor to investigate the source of errors on their end and develop a plan to minimize these issues moving forward.

3. Collaborate with the product manager to increase the number of subscriptions that actually reach and engage with the payment portal. Since many users drop off before even attempting payment, this represents a significant loss early in the funnel. Consider strategies like payment reminders or outreach from customer service agents to encourage completion.

![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/image1.png)
![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/image2.png)
![Data Model](https://github.com/hoomanvahdat0-DataAnalysis/Payment_Funnel_Analysis_SaaS_FinTech/blob/main/image3.png)

## Next Steps:
Dig deeper into the error breakdown to identify which issues occur most frequently, distinguishing between user-related errors and those originating from the vendor.

Examine why many subscriptions never initiate the payment process. Determine whether this is due to internal process gaps or if customers are simply forgetting to complete the payment step.
