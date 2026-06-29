import pandas as pd
import matplotlib.pyplot as plt
df_clean = pd.read_csv(
    "cleaned_retail.csv"
)
df_clean["InvoiceDate"] = pd.to_datetime(
    df_clean["InvoiceDate"]
)
#Total Revenue
total_revenue = df_clean["Revenue"].sum()
print(f"Total Revenue: ${total_revenue:,.2f}") 

#Unique Customers
customers = df_clean["CustomerID"].nunique()
print(f"Unique Customers: {customers}")

#Unique Orders
orders = df_clean["InvoiceNo"].nunique()
print(f"Unique Orders: {orders}")

#Average Order Value
aov = (
    df_clean
    .groupby("InvoiceNo")["Revenue"]
    .sum()
    .mean()
)
print(f"Average Order Value: ${aov:,.2f}")

#Revenue per customer
rpc = total_revenue / customers
print(
    f"Revenue Per Customer: ${rpc:,.2f}"
)

#revenue analysis month-year
df_clean["YearMonth"] = (
    df_clean["InvoiceDate"]
    .dt.to_period("M")
)

#revenue analysis monthly
monthly_revenue = (
    df_clean.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
)
monthly_revenue.head()
print("\nMonthly Revenue:")
print(monthly_revenue)

monthly_revenue["Revenue"].agg([
    "min",
    "max",
    "mean",
    "median"
])

top_products = (
    df_clean
    .groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)
print(top_products)

country_revenue = (
    df_clean
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
print(country_revenue.head(15))

customer_revenue = (
    df_clean.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

pareto = customer_revenue.reset_index()

pareto["CumulativeRevenue"] = (
    pareto["Revenue"].cumsum()
)

pareto["CumulativePct"] = (
    pareto["CumulativeRevenue"]
    /
    pareto["Revenue"].sum()
)

customers_80 = (
    pareto["CumulativePct"] <= 0.8
).sum()

pct_customers = (
    customers_80 /
    len(pareto)
) * 100

print(
    f"{pct_customers:.2f}% of customers generate 80% of revenue"
)

top10_share = (
    customer_revenue.head(10).sum()
    /
    customer_revenue.sum()
) * 100

top50_share = (
    customer_revenue.head(50).sum()
    /
    customer_revenue.sum()
) * 100

top100_share = (
    customer_revenue.head(100).sum()
    /
    customer_revenue.sum()
) * 100
print(top10_share)
print(top50_share)
print(top100_share)

monthly_revenue.plot(
    x="Month",
    y="Revenue",
    kind="line",
    figsize=(10,5)
)
plt.show()
