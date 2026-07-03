# Customer Retention Analytics 

## Overview

This project is an end-to-end customer analytics solution built using Python, SQL, and Power BI to analyze customer purchasing behavior, identify high-value customers, estimate Customer Lifetime Value (CLV), detect churn risk, and recommend targeted retention strategies.

The project combines data cleaning, SQL analysis, customer segmentation, business intelligence dashboards, and actionable insights to demonstrate how analytics can support customer retention and revenue growth in an e-commerce business.

---

## Business Problem

Acquiring new customers is significantly more expensive than retaining existing ones. Businesses need to understand:

* Who are the most valuable customers?
* Which customers are likely to churn?
* How much revenue is at risk?
* Which retention strategy should be used for each customer segment?

This project answers those questions using data-driven customer analytics.

---

## Dataset

The project uses the **Online Retail** transactional dataset from the UCI Machine Learning Repository.

The dataset contains:

* Customer purchases
* Invoice information
* Product details
* Quantity purchased
* Unit prices
* Transaction dates
* Customer location

---

## Tech Stack

* Python
* Pandas
* NumPy
* SQLite
* SQL
* Matplotlib
* Power BI

---

# Data Cleaning

The dataset was cleaned by:

* Removing cancelled transactions
* Removing missing Customer IDs
* Removing negative quantities
* Creating a Revenue column
* Converting InvoiceDate into datetime format

---

# SQL Analysis

Business insights generated using SQLite include:

* Revenue by country
* Top-selling products
* Monthly revenue trend
* Top customers by revenue
* Average order value

---

# Customer Segmentation (RFM Analysis)

Customers were segmented using:

* **Recency** – Days since last purchase
* **Frequency** – Number of purchases
* **Monetary** – Total customer spending

The resulting customer segments include:

* Champions
* Loyal Customers
* Potential Loyalists
* At Risk
* Lost Customers

---

# Churn Analysis

Customers with no purchases for more than **90 days** were classified as churned.

The analysis includes:

* Churn rate
* Revenue at risk
* Customer priority levels
* High-risk customer identification

---

# Power BI Dashboard

The interactive dashboard provides:

* Executive KPI cards
* Revenue by customer segment
* Customer distribution by segment
* Revenue contribution by segment
* Revenue at risk by retention action
* Top customers by CLV
* Interactive filters for Country, Segment, and Churn

Dashboard: <img width="580" height="329" alt="dashboard" src="https://github.com/user-attachments/assets/fe92a428-d7ca-4801-84cf-ebb0af545976" />



---

# Key Business Insights

* Champions generated the largest share of overall revenue.
* Approximately one-third of customers were identified as churned.
* More than $3 million in customer value was identified as revenue at risk.
* Win-back offers and discount campaigns represent the highest-impact retention opportunities.
* Customer segmentation enables personalized marketing strategies that can improve retention and maximize customer lifetime value.

---

# Future Improvements

* Predict churn using machine learning models.
* Deploy an interactive dashboard using Streamlit.
* Integrate cloud data storage.
* Automate the analytics pipeline using scheduled ETL workflows.
* Build real-time customer monitoring dashboards.

---
