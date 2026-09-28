# Calculate detailed metrics
print("=== DETAILED FUNNEL & ERROR ANALYSIS ===")

# In Subscriptions.csv:
# Status distribution:
# NaN (Uninitiated): 24
# Status 1 (Widget Opened): 7
# Status 2 (Payment Entered): 2
# Status 4 (Payment Success / Pending complete): 1
# Status 0 (Error): 4
# Status 5 (Complete / Paid): 12

total_subs = 50
total_rev = subs['Revenue'].sum()

uninitiated_rev = subs[subs['Current Payment Status'].isna()]['Revenue'].sum()
widget_opened_rev = subs[subs['Current Payment Status'] == 1.0]['Revenue'].sum()
entered_rev = subs[subs['Current Payment Status'] == 2.0]['Revenue'].sum()
error_rev = subs[subs['Current Payment Status'] == 0.0]['Revenue'].sum()
success_rev = subs[subs['Current Payment Status'] == 4.0]['Revenue'].sum()
complete_rev = subs[subs['Current Payment Status'] == 5.0]['Revenue'].sum()

unconverted_subs = total_subs - 12
unconverted_rev = total_rev - complete_rev

print(f"Total Subscriptions: {total_subs}, Total Potential Revenue: ${total_rev:,.2f}")
print(f"Converted Subscriptions: 12 (24.0%), Realized Revenue: ${complete_rev:,.2f} ({complete_rev/total_rev*100:.1f}%)")
print(f"Unconverted Subscriptions: {unconverted_subs} (76.0%), Lost/Stuck Revenue: ${unconverted_rev:,.2f} ({unconverted_rev/total_rev*100:.1f}%)")

print("\nBreakdown of Unconverted:")
print(f"1. Uninitiated (NaN): 24 subs (48%), ${uninitiated_rev:,.2f}")
print(f"2. Abandoned at Widget Opened (Status 1): 7 subs (14%), ${widget_opened_rev:,.2f}")
print(f"3. Stuck at Payment Entered (Status 2): 2 subs (4%), ${entered_rev:,.2f}")
print(f"4. Stuck in Error (Status 0): 4 subs (8%), ${error_rev:,.2f}")
print(f"5. Stuck at Payment Success (Status 4): 1 subs (2%), ${success_rev:,.2f}")

# Check Vendor vs User error in Log:
# Sub 38499: 1 -> 2 -> 3 -> 4 -> 0 (Error after PaymentSuccess = Vendor sync / webhook error)
# Sub 44467: 1 -> 2 -> 3 -> 0 (User/Card error at submission) -> retried -> 2 -> 3 -> 4 -> 5 (Success)
# Sub 51992: Out of order / retry after status 5 -> error -> 2
# Sub 74773: Status 5 -> error -> retry -> status 5
# Sub 99332: 1 -> 2 -> 3 -> 0 (Error at submission = User or Vendor auth error)