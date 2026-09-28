# Analyze Subscriptions and Payment Status Log deeply
ps_log = pd.read_csv('Payment_Status_Log.csv')
ps_def = pd.read_csv('Payment_Status_Definitions.csv')
subs = pd.read_csv('Subscriptions.csv')

ps_log['Movement_Date'] = pd.to_datetime(ps_log['Movement_Date'])
ps_log = ps_log.sort_values(by=['Subscription_ID', 'Movement_Date'])

# Merge definitions
ps_log_merged = ps_log.merge(ps_def, on='Status_ID', how='left')

print("Payment Status Definitions:")
print(ps_def)

print("\n--- All Subscriptions in Payment Status Log ---")
grouped = ps_log_merged.groupby('Subscription_ID')
for sub_id, group in grouped:
    print(f"\nSub ID: {sub_id}")
    print(group[['Status_ID', 'Description', 'Movement_Date']].to_string(index=False))

print("\n--- Subscriptions Overview ---")
print("Total subscriptions in Subscriptions table:", len(subs))
print("Current Payment Status value counts in Subscriptions table:")
print(subs['Current Payment Status'].value_counts(dropna=False))

# Let's inspect subscriptions with Current Payment Status
print("\nSubscriptions with Current Payment Status breakdown:")
print(subs[['Subscription ID', 'Product_ID', 'Current Payment Status', 'Revenue', 'Active']].merge(
    ps_def, left_on='Current Payment Status', right_on='Status_ID', how='left'
).head(20))