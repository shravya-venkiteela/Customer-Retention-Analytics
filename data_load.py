import pandas as pd

df = pd.read_excel("Online Retail.xlsx")

#Find negative quantities
negative_qty = df[df["Quantity"] < 0]

print("Negative Quantity Rows:")
print(len(negative_qty))

print("\nSample Negative Quantity Records:")
print(
    negative_qty[
        ["InvoiceNo","Quantity","UnitPrice"]
    ].head(10)
)

print("\nInvoice Prefix Check:")
print(
    negative_qty["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
    .value_counts()
)

#cleaning the data
df_clean = df.copy()

#remove missing customer IDs
df_clean = df_clean.dropna(subset=["CustomerID"])

#remove duplicates
df_clean = df_clean.drop_duplicates()

#remove cancellations
df_clean = df_clean[
    ~df_clean["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

#remove negative quantities
df_clean = df_clean[
    df_clean["Quantity"] > 0
]

#remove invalid prices
df_clean = df_clean[
    df_clean["UnitPrice"] > 0
]

#revenue feature
df_clean["Revenue"] = (
    df_clean["Quantity"] *
    df_clean["UnitPrice"]
)

print("Final Shape:", df_clean.shape)

df_clean.to_csv(
    "cleaned_retail.csv",
    index=False
)