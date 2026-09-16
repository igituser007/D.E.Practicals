"""
Practical 10: Mini Project - End-to-End Data Engineering Solution
----------------------------------------------------------------
A small but complete data engineering pipeline for a fictional retail
store, covering every stage asked for in the mini project brief:

  1. Data Ingestion    - read raw sales (CSV) and customer (JSON) data
  2. Data Cleaning     - handle missing values, duplicates, invalid rows
  3. Transformation    - compute derived fields, standardize formats
  4. Storage           - load into a SQLite data warehouse
  5. Data Warehouse    - simple star schema (dimension + fact tables)
  6. Reporting         - aggregated report + a chart
"""

import os
import json
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)
DB_PATH = "output/retail_warehouse.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)

# ============================================================
# STAGE 1: DATA INGESTION
# ============================================================
print("=" * 60)
print("STAGE 1: DATA INGESTION")
print("=" * 60)

# Raw sales transactions (CSV) - includes messy real-world issues on purpose
sales_csv = """sale_id,customer_id,product,category,quantity,unit_price,sale_date
1,1,Pen,Stationery,10,10,2026-01-05
2,2,Notebook,Stationery,5,40,2026-01-06
3,1,Pen,Stationery,10,10,2026-01-05
4,3,Mouse,Electronics,2,700,2026-01-07
5,4,Bag,Accessories,1,500,2026-01-08
6,2,Notebook,Stationery,,40,2026-01-09
7,5,Mouse,Electronics,-1,700,2026-01-10
8,1,Bag,Accessories,2,500,2026-02-01
9,3,Pen,Stationery,20,10,2026-02-02
10,6,Notebook,Stationery,3,40,2026-02-03
"""
with open("data/sales.csv", "w") as f:
    f.write(sales_csv)

# Raw customer data (JSON) - one record has a missing name
customers_json = [
    {"customer_id": 1, "name": "Riya", "city": "Pune"},
    {"customer_id": 2, "name": "Amit", "city": "Mumbai"},
    {"customer_id": 3, "name": None, "city": "Delhi"},
    {"customer_id": 4, "name": "Neha", "city": "Pune"},
    {"customer_id": 5, "name": "Karan", "city": "Mumbai"},
    {"customer_id": 6, "name": "Zoya", "city": "Delhi"},
]
with open("data/customers.json", "w") as f:
    json.dump(customers_json, f)

raw_sales = pd.read_csv("data/sales.csv")
with open("data/customers.json") as f:
    raw_customers = pd.json_normalize(json.load(f))

print(f"\nIngested {len(raw_sales)} raw sales rows and {len(raw_customers)} raw customer rows.")
print("\nRaw sales sample:")
print(raw_sales)


# ============================================================
# STAGE 2: DATA CLEANING
# ============================================================
print("\n" + "=" * 60)
print("STAGE 2: DATA CLEANING")
print("=" * 60)

customers = raw_customers.copy()
customers["name"] = customers["name"].fillna("Unknown")

sales = raw_sales.copy()
before = len(sales)

# Drop duplicate rows
sales = sales.drop_duplicates(subset=["customer_id", "product", "sale_date"])

# Fill missing quantity with 0, then drop rows that make no business sense
sales["quantity"] = sales["quantity"].fillna(0)
sales = sales[sales["quantity"] > 0]

after = len(sales)
print(f"\nRemoved {before - after} rows (duplicates, missing/invalid quantity).")
print("\nCleaned sales:")
print(sales)


# ============================================================
# STAGE 3: TRANSFORMATION
# ============================================================
print("\n" + "=" * 60)
print("STAGE 3: TRANSFORMATION")
print("=" * 60)

sales["sale_date"] = pd.to_datetime(sales["sale_date"])
sales["sale_month"] = sales["sale_date"].dt.to_period("M").astype(str)
sales["revenue"] = sales["quantity"] * sales["unit_price"]

print("\nTransformed sales (added sale_month and revenue):")
print(sales)


# ============================================================
# STAGE 4 & 5: STORAGE + DATA WAREHOUSE DESIGN (star schema)
# ============================================================
print("\n" + "=" * 60)
print("STAGE 4 & 5: STORAGE INTO A STAR-SCHEMA DATA WAREHOUSE")
print("=" * 60)

# Dimension: customers
dim_customers = customers[["customer_id", "name", "city"]]
dim_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)

# Dimension: products (derived from the sales data itself)
dim_products = (
    sales[["product", "category"]]
    .drop_duplicates()
    .reset_index(drop=True)
    .rename_axis("product_key")
    .reset_index()
)
dim_products.to_sql("dim_products", conn, if_exists="replace", index=False)

# Fact table: one row per sale, linked to the dimensions via keys
fact_sales = sales.merge(dim_products, on=["product", "category"], how="left")
fact_sales = fact_sales[[
    "sale_id", "customer_id", "product_key", "sale_date",
    "sale_month", "quantity", "unit_price", "revenue",
]]
fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

print("\nWarehouse tables created: dim_customers, dim_products, fact_sales")
print("\ndim_products:")
print(dim_products)


# ============================================================
# STAGE 6: REPORTING
# ============================================================
print("\n" + "=" * 60)
print("STAGE 6: REPORTING")
print("=" * 60)

report_query = """
SELECT
    c.city,
    p.category,
    SUM(f.revenue) AS total_revenue,
    SUM(f.quantity) AS total_units
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_products p ON f.product_key = p.product_key
GROUP BY c.city, p.category
ORDER BY total_revenue DESC
"""
report = pd.read_sql(report_query, conn)
print("\nRevenue by city and category:")
print(report)
report.to_csv("output/revenue_by_city_category.csv", index=False)

monthly_revenue = pd.read_sql(
    "SELECT sale_month, SUM(revenue) AS total_revenue FROM fact_sales GROUP BY sale_month ORDER BY sale_month",
    conn,
)
print("\nRevenue by month:")
print(monthly_revenue)
monthly_revenue.to_csv("output/monthly_revenue.csv", index=False)

# Chart: monthly revenue trend
plt.figure(figsize=(6, 4))
plt.bar(monthly_revenue["sale_month"], monthly_revenue["total_revenue"], color="steelblue")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("output/monthly_revenue_chart.png")
plt.close()

# Chart: revenue by category
category_revenue = pd.read_sql(
    "SELECT p.category, SUM(f.revenue) AS total_revenue FROM fact_sales f "
    "JOIN dim_products p ON f.product_key = p.product_key GROUP BY p.category",
    conn,
)
plt.figure(figsize=(6, 4))
plt.bar(category_revenue["category"], category_revenue["total_revenue"], color="darkorange")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("output/category_revenue_chart.png")
plt.close()

conn.close()
print("\nSaved reports (CSV) and charts (PNG) to the output/ folder.")
print("Mini project pipeline complete.")
