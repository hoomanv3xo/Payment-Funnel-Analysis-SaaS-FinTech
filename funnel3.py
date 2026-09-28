# Analyze the errors and funnel metrics across Subscriptions dataset and Payment Status Log dataset
# Subscriptions dataset analysis
print("--- ANALYSIS OF SUBSCRIPTIONS TABLE (N=50) ---")
status_counts = subs['Current Payment Status'].value_counts(dropna=False)
print(status_counts)

total_subs = len(subs)
completed = subs[subs['Current Payment Status'] == 5.0]
errors = subs[subs['Current Payment Status'] == 0.0]
opened = subs[subs['Current Payment Status'] == 1.0]
entered = subs[subs['Current Payment Status'] == 2.0]
success_not_complete = subs[subs['Current Payment Status'] == 4.0]
nan_status = subs[subs['Current Payment Status'].isna()]

print(f"Total Subscriptions: {total_subs}")
print(f"Completed (Status 5): {len(completed)} ({len(completed)/total_subs*100:.1f}%)")
print(f"Error (Status 0): {len(errors)} ({len(errors)/total_subs*100:.1f}%)")
print(f"Widget Opened (Status 1): {len(opened)} ({len(opened)/total_subs*100:.1f}%)")
print(f"Payment Entered (Status 2): {len(entered)} ({len(entered)/total_subs*100:.1f}%)")
print(f"Payment Success (Status 4): {len(success_not_complete)} ({len(success_not_complete)/total_subs*100:.1f}%)")
print(f"Uninitiated / NaN: {len(nan_status)} ({len(nan_status)/total_subs*100:.1f}%)")

# Let's check revenue lost / stuck
print("\nRevenue distribution by Current Payment Status:")
print(subs.groupby('Current Payment Status')['Revenue'].agg(['count', 'sum', 'mean']))

# Analysis of Payment Status Log (N=12 unique subscriptions)
print("\n--- ANALYSIS OF PAYMENT STATUS LOG (N=12 subscriptions) ---")
# Latest status for each sub in Payment Status Log
latest_log = ps_log.groupby('Subscription_ID').last().reset_index()
latest_log = latest_log.merge(ps_def, on='Status_ID', how='left')
print("Latest status in Payment Status Log:")
print(latest_log[['Subscription_ID', 'Status_ID', 'Description', 'Movement_Date']])

# Check if errors occurred anytime during log
error_subs = ps_log[ps_log['Status_ID'] == 0]['Subscription_ID'].unique()
print(f"\nSubscriptions that experienced an Error (Status 0) in log: {error_subs} (Count: {len(error_subs)})")

# Details on error subscriptions in log
for sub_id in error_subs:
    sub_events = ps_log[ps_log['Subscription_ID'] == sub_id].sort_values('Movement_Date')
    print(f"\nTimeline for Error Sub {sub_id}:")
    for _, row in sub_events.iterrows():
        desc = ps_def[ps_def['Status_ID'] == row['Status_ID']]['Description'].values[0]
        print(f"  {row['Movement_Date']} - Status {row['Status_ID']}: {desc}")