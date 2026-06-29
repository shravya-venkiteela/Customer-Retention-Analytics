import pandas as pd
import numpy as np
df = pd.read_excel('Online Retail.xlsx')
missing_df = pd.DataFrame({"Missing Count": df.isnull().sum(), "Missing Percentage": round(df.isnull().sum() / len(df) * 100, 2)})
print(missing_df)

duplicates = df.duplicated().sum()
print(f"Duplicate Rows: {duplicates}")

negative_qty_count = (df["Quantity"] < 0).sum()
print(f"Negative Quantity Rows: {negative_qty_count}")

negative_price_count = (df["UnitPrice"] < 0).sum()
print(f"Negative Price Rows: {negative_price_count}")

negative_qty = df[df["Quantity"] < 0]
negative_qty[["InvoiceNo", "Description", "Quantity", "UnitPrice"]].head(20)

negative_qty["InvoiceNo"].astype(str).str.startswith("C").value_counts()


df = df.dropna(subset=["CustomerID"])
df = df.drop_duplicates()

print("\nInvoice Numbers Starting With C:")

negative_non_c = df[
    (df["Quantity"] < 0) &
    (~df["InvoiceNo"].astype(str).str.startswith("C"))
]

print(negative_non_c.shape)

negative_non_c[
    [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "CustomerID"
    ]
].head(20)