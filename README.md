# Payment Funnel Analysis: Finding and Fixing Unpaid Subscription Friction

## Executive Summary

This analysis looks at where customers drop out of the payment process. Only **8 of 12** customers who opened the payment widget entered payment details (66.7%), and only **4 reached `Complete`** (33.3%). The biggest drop happens before payment details are entered.

There is also a problem after payment succeeds. **6 subscriptions recorded `PaymentSuccess`, but only 4 reached `Complete`**. This means 2 successful payments may not have been properly recorded internally.

Unpaid subscriptions appear to be caused mainly by early payment abandonment/form friction, possible payment-provider errors, and internal reconciliation issues after successful payments. Of the subscriptions with known payment status, 14 of 26 are unpaid, representing $168,500 in revenue. Another 24 subscriptions have no payment status, so the actual unpaid amount may be higher.

## Business Problem

Customers become converted only after completing payment. Unpaid subscriptions reduce revenue and lower the conversion rate.

The business needs to understand:

* Where customers stop or fail.
* Whether failures are customer or payment-provider related.
* Which subscriptions need follow-up.
* How much revenue is at risk.
* 
![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/data model.png).
![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/payment funnel stages.png).


## Methodology

`Complete` is used as the final conversion event because it confirms the payment was completed internally.

| Milestone             | Subscriptions |   Rate |
| --------------------- | ------------: | -----: |
| Payment widget opened |            12 | 100.0% |
| Payment entered       |             8 |  66.7% |
| Payment submitted     |             7 |  58.3% |
| Payment success       |             6 |  50.0% |
| Complete              |             4 |  33.3% |

For reporting, use `Subscription_ID` to track each customer journey and sort events by `Movement_Date`. Keep both the payment attempt history and the final subscription outcome.

Do not treat status numbers as a simple ranking because customers can retry, move backward, or encounter errors at different stages.

## Skills 

* **SQL:** CTEs, joins, CASE statements, aggregates
* **Python:** Pandas, Matplotlib, NumPy, functions, funnel analysis, statistics

## Results & Recommendations

### 1. Improve the payment form experience

**4 of 12** widget opens never reached `PaymentEntered`, making this the largest drop.

Check:

* Payment widget loading
* Mobile experience
* Session or authentication issues
* Payment-method availability
* Payment button reliability

Add tracking for widget loading, failures, and form starts to identify the real cause.

### 2. Fix successful-payment reconciliation

**2 of 6** successful payments did not reach `Complete`.

This could be caused by a webhook, system update, or similar issue. Create an alert when `PaymentSuccess` is not followed by `Complete` within 15 minutes, then automatically retry or send the case to operations.

### 3. Investigate payment errors

There were **5 error events**. Three happened after `PaymentSubmitted`, which may indicate payment-provider problems.

However, the current data does not show whether errors came from the customer, payment provider, or internal system.

Add error sources and response codes before assigning responsibility.

### 4. Recover known unpaid revenue

There are **14 known unpaid subscriptions worth $168,500**.

Use different follow-up actions based on the customer's last stage:

* **Before payment:** send a reminder and payment link.
* **Form issues:** provide clearer validation and instructions.
* **Payment-provider failure:** offer a retry.
* **Payment success but not complete:** reconcile first before contacting the customer.

## Next Steps

1. Add `payment_attempt_id`, `error_source`, `error_code`, `vendor_transaction_id`, payment method, and reconciliation status.
2. Track key events such as widget loaded, form started, validation failed, submit clicked, vendor response, and completion.
3. Create alerts and a dashboard for stuck payments 

![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/payment_funnel_conversion.png)
![Data Model](https://github.com/hoomanv3xo/Payment-Funnel-Analysis-SaaS_FinTech/blob/main/payment_error_context.png)


## Next Steps:
1. Investigate the Submitted→Success gap as a payments-operations issue — likely causes include card declines, gateway timeouts, or fraud verification failures.
2. Treat Success→Complete as an engineering bug, not a UX fix — payment already succeeds at this point, so the order simply isn't finalizing.
3. Handle post-purchase churn as a separate workstream from the order funnel — since "not useful" outranks "expensive" as a cancelation reason, this points to an onboarding/activation gap rather than a pricing problem.
