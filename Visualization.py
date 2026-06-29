import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(
    "cleaned_retail.csv", 
    parse_dates=["InvoiceDate"]
)

df["YearMonth"] = (
    df["InvoiceDate"].dt.to_period("M").astype(str)
)
monthly_revenue = (
    df.groupby("YearMonth")["Revenue"].sum()
    .reset_index()
)
plt.figure(figsize=(10,5))
plt.plot(
    monthly_revenue["YearMonth"],
    monthly_revenue["Revenue"],
    color="green",
    marker="o"
)
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.savefig("monthly_revenue.png")
plt.show()

country_revenue = (
    df[df["Country"] != "United Kingdom"]
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
plt.figure(figsize=(10,5))
plt.bar(
    country_revenue.index,
    country_revenue.values,
    color="blue"
)
plt.title("Top 10 Countries by Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("countries_revenue.png")
plt.show()

rfm = pd.read_csv("rfm_results.csv")
segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
    .sum()
    .sort_values(ascending=False)
)
plt.figure(figsize=(10,5))
plt.bar(
    segment_revenue.index,
    segment_revenue.values,
    color="orange"
)
plt.title("Revenue by Customer Segment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("segment_revenue.png")
plt.show()

#Customer Distribution by Segment

segment_count = (
    rfm["Segment"]
    .value_counts()
    .reindex([
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "At Risk",
        "Lost Customers"
    ])
)

plt.figure(figsize=(9,5))

plt.bar(
    segment_count.index,
    segment_count.values,
    color=["green","blue","orange","red","gray"]
)

plt.title("Customer Distribution by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=20)
for i, value in enumerate(segment_count.values):
    plt.text(i, value+20, str(value), ha="center")

plt.tight_layout()
plt.savefig("segment_distribution.png")
plt.show()

revenue_at_risk = (
    rfm.groupby("Segment")["RevenueAtRisk"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

plt.bar(
    revenue_at_risk.index,
    revenue_at_risk.values,
    color="yellow"
)

plt.title("Revenue at Risk by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue at Risk ($)")

plt.xticks(rotation=20)

plt.tight_layout()
plt.savefig("revenue_at_risk.png")
plt.show()
rfm["Churn"].value_counts().plot(
    kind="bar",
    color="red"
)
churn_counts = rfm["Churn"].value_counts().sort_index()

plt.figure(figsize=(6,4))
plt.bar(
    ["Active","Churned"],
    churn_counts.values,
    color=["green","red"]
)
plt.title("Customer Churn Distribution")
plt.ylabel("Customers")
plt.xlabel("Churn Status")
plt.tight_layout()
plt.savefig("churn_distribution.png")
plt.show()