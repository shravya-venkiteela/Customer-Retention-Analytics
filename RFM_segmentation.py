from datetime import timedelta
import pandas as pd
import numpy as np

from retention_strategy import retention_action
df_clean = pd.read_csv(
    "cleaned_retail.csv"
)
df_clean["InvoiceDate"] = pd.to_datetime(
    df_clean["InvoiceDate"]
)
snapshot_date = (df_clean["InvoiceDate"].max() 
                 + timedelta(days=1))
print(snapshot_date)

rfm = df_clean.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "InvoiceNo": "nunique",
    "Revenue": "sum"
})
rfm.columns = ["Recency", "Frequency", "Monetary"]
rfm = rfm.reset_index()
print(rfm.columns)
print(rfm.describe())

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q = 4,
    labels=[4,3,2,1]
)
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q = 4,
    labels=[1,2,3,4]
)
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q = 4,
    labels=[1,2,3,4]
)
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)
print(rfm.head())

#Segementation og the customers
def segment_customer(row):

    r = int(row["R_Score"])
    f = int(row["F_Score"])

    if r == 4 and f == 4:
        return "Champions"

    elif r >= 3 and f >= 3:
        return "Loyal Customers"

    elif r >= 3 and f <= 2:
        return "Potential Loyalists"

    elif r <= 2 and f >= 3:
        return "At Risk"

    else:
        return "Lost Customers"
rfm["Segment"] = rfm.apply(
    segment_customer,
    axis=1
)

segment_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("Segment","count"),
        AvgRevenue=("Monetary","mean"),
        TotalRevenue=("Monetary","sum"),
        AvgRecency=("Recency","mean"),
        AvgFrequency=("Frequency","mean")
    )
    .sort_values(
        "TotalRevenue",
        ascending=False
    )
)
print(segment_summary)

segment_summary["RevenueSharePct"] = (
    segment_summary["TotalRevenue"]
    /
    segment_summary["TotalRevenue"].sum()
) * 100
print(segment_summary.to_string())

rfm["CLV"] = (
    rfm["Monetary"] *
    rfm["Frequency"]
)
clv_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("Segment","count"),
        AvgCLV=("CLV","mean"),
        TotalCLV=("CLV","sum")
    )
    .sort_values(
        "TotalCLV",
        ascending=False
    )
)

rfm["Churn"] = (
    rfm["Recency"] > 90
).astype(int)

print(rfm["Churn"].value_counts())

print(
    rfm["Churn"]
    .value_counts(normalize=True)
)

print(clv_summary)
rfm["RevenueAtRisk"] = np.where(
    rfm["Churn"] == 1,
    rfm["CLV"],
    0
)

total_risk = rfm["RevenueAtRisk"].sum()
print(
    f"Total Revenue At Risk: ${total_risk:,.2f}"
)

risk_by_segment = (
    rfm.groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        RevenueAtRisk=("RevenueAtRisk", "sum")
    )
    .sort_values(
        "RevenueAtRisk",
        ascending=False
    )
)
print(risk_by_segment)


rfm.to_csv(
    "rfm_customer_segments.csv",
    index=True
)

rfm["RecommendedAction"] = rfm["Segment"].apply(retention_action)
print(
    rfm[
        ["Segment","RecommendedAction"]
    ].head(10)
)

rfm["CLV_Score"] = pd.qcut(
    rfm["CLV"],
    q=4,
    labels=[1,2,3,4]
).astype(int)

rfm["PriorityScore"] = (
    rfm["Churn"] * 70
    +
    rfm["CLV_Score"] * 10
)

def priority_level(score):

    if score >= 100:
        return "Critical"

    elif score >= 90:
        return "High"

    elif score >= 80:
        return "Medium"

    else:
        return "Low"
rfm["PriorityLevel"] = (
    rfm["PriorityScore"]
    .apply(priority_level)
)
print(
    rfm[
        [
            "CustomerID",
            "Segment",
            "CLV",
            "Churn",
            "RecommendedAction",
            "PriorityLevel"
        ]
    ].head(20)
)
strategy_summary = (
    rfm.groupby(
        [
            "PriorityLevel",
            "RecommendedAction"
        ]
    )
    .agg(
        Customers=("CustomerID","count"),
        Revenue=("Monetary","sum")
    )
    .reset_index()
)

print(strategy_summary)
rfm.to_csv(
    "customer_retention_strategy.csv",
    index=False
)

rfm.to_csv(
    "rfm_customer_analytics.csv",
    index=False
)
action_summary = (
    rfm.groupby(
        "RecommendedAction"
    )
    .agg(
        Customers=("CustomerID", "count"),
        RevenueAtRisk=("RevenueAtRisk", "sum")
    )
    .sort_values(
        "RevenueAtRisk",
        ascending=False
    )
)
print(action_summary)

top_20_risk = (
    rfm.sort_values(
        by="RevenueAtRisk",
        ascending=False
    )
    .head(20)
)
print(
    top_20_risk[
        [
            "CustomerID",
            "Segment",
            "CLV",
            "RevenueAtRisk",
            "RecommendedAction",
            "PriorityLevel"
        ]
    ]
)

# Add customer's country
customer_country = (
    df_clean.groupby("CustomerID")["Country"]
    .first()
    .reset_index()
)

rfm = rfm.merge(
    customer_country,
    on="CustomerID",
    how="left"
)


rfm.to_csv( "rfm_results.csv", index=False)
print(rfm.columns)
print(rfm[["CustomerID", "Country"]].head())
print(df_clean.columns)