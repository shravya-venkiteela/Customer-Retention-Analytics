import pandas as pd
import sqlite3
df_clean = pd.read_csv(
    "cleaned_retail.csv"
)
conn = sqlite3.connect("retail_data.db")
df_clean.to_sql("retail", conn, if_exists="replace", index=False)


#revenue by country
query = """
SELECT Country, ROUND(SUM(Revenue),2) AS Revenue
FROM retail
GROUP BY Country
ORDER BY Revenue DESC;

"""
country_revenue = pd.read_sql_query(query, conn)
print(country_revenue.head(10))

#Top10 products
query = """
SELECT Description, ROUND(SUM(Revenue),2) AS Revenue
FROM retail
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 20;
"""

top_products = pd.read_sql_query(query, conn)
print(top_products.head(10))


#Monthly revenue trend
query = """
SELECT strftime('%Y-%m', InvoiceDate) AS Month, ROUND(SUM(Revenue),2) AS Revenue
FROM retail
GROUP BY Month
ORDER BY Month;
"""
monthly_revenue = pd.read_sql_query(query, conn)
print(monthly_revenue)


#Top Customers
query = """
SELECT CustomerID, ROUND(SUM(Revenue),2) AS Revenue
FROM retail
GROUP BY CustomerID
ORDER BY Revenue DESC
LIMIT 20;
"""
top_customers = pd.read_sql_query(query, conn)
print(top_customers)

#Average Order Value
query = """
SELECT ROUND(SUM(Revenue)/COUNT(DISTINCT InvoiceNo),2) AS AverageOrderValue
FROM retail;
"""
aov = pd.read_sql_query(query, conn)
print(aov)
conn.close()