"""
Practical 09: End-to-End Data Pipeline
------------------------------------
A single combined practical covering three related tasks:
  1. End-to-end pipeline: CSV -> Pandas -> Data Cleaning -> SQL Database -> Report
  2. An ETL pipeline for an e-commerce dataset (customers, orders, products, payments)
  3. A data pipeline that handles both historical and newly arriving data
"""

import os
import sqlite3
import pandas as pd

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)
DB_PATH = "output/ecommerce_warehouse.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("TASK 1 & 2: E-commerce ETL Pipeline (CSV -> Clean -> SQL -> Report)")
print("=" * 60)

# -----------------------------
# Extract: create sample e-commerce CSVs
# -----------------------------
pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name": ["Riya", "Amit", None, "Neha"],
    "city": ["Pune", "Mumbai", "Delhi", "Pune"],
}).to_csv("data/customers.csv", index=False)

pd.DataFrame({
    "product_id": [101, 102, 103],
    "product_name": ["Pen", "Notebook", "Bag"],
    "unit_price": [10.0, 40.0, 500.0],
}).to_csv("data/products.csv", index=False)

pd.DataFrame({
    "order_id": [1001, 1002, 1003, 1004],
    "customer_id": [1, 2, 3, 4],
    "product_id": [101, 102, 999, 103],  # 999 is an invalid product_id
    "quantity": [5, 2, 1, -1],           # -1 is an invalid quantity
}).to_csv("data/orders.csv", index=False)

pd.DataFrame({
    "order_id": [1001, 1002, 1004],
    "amount_paid": [50.0, 80.0, 500.0],
    "status": ["paid", "paid", "paid"],
}).to_csv("data/payments.csv", index=False)

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
payments = pd.read_csv("data/payments.csv")

print("\nRaw orders:")
print(orders)

# -----------------------------
# Clean & Transform
# -----------------------------
customers["name"] = customers["name"].fillna("Unknown")

# Remove orders referencing a product that doesn't exist, and non-positive quantities
valid_orders = orders[
    orders["product_id"].isin(products["product_id"]) & (orders["quantity"] > 0)
].copy()

print("\nCleaned orders (invalid product_id / quantity removed):")
print(valid_orders)

# Merge everything into one denormalized fact table for reporting
merged = (
    valid_orders
    .merge(customers, on="customer_id", how="left")
    .merge(products, on="product_id", how="left")
    .merge(payments, on="order_id", how="left")
)
merged["order_total"] = merged["quantity"] * merged["unit_price"]

print("\nMerged e-commerce fact table:")
print(merged)

# -----------------------------
# Load into SQL database (star-schema-ish: dimensions + fact table)
# -----------------------------
customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
products.to_sql("dim_products", conn, if_exists="replace", index=False)
merged.to_sql("fact_orders", conn, if_exists="replace", index=False)

# -----------------------------
# Report: simple aggregated summary
# -----------------------------
report = merged.groupby("city", dropna=False)["order_total"].sum().reset_index()
report.columns = ["city", "total_revenue"]
print("\nReport - Revenue by city:")
print(report)

report.to_csv("output/revenue_by_city_report.csv", index=False)


print("\n" + "=" * 60)
print("TASK 3: Pipeline Handling Historical + Newly Arriving Data")
print("=" * 60)

# "Historical" load: what we already loaded above becomes day 0 history
history_ids = pd.read_sql("SELECT order_id FROM fact_orders", conn)["order_id"].tolist()
print(f"\nHistorical orders already in the warehouse: {history_ids}")

# New data arrives later (some overlap with history, some genuinely new)
new_batch = pd.DataFrame({
    "order_id": [1002, 1005, 1006],   # 1002 is a duplicate of history, 1005/1006 are new
    "customer_id": [2, 1, 4],
    "product_id": [102, 101, 103],
    "quantity": [3, 2, 1],
})

new_batch_valid = new_batch[
    new_batch["product_id"].isin(products["product_id"]) & (new_batch["quantity"] > 0)
].copy()

# Only keep rows that are NOT already in history (incremental merge)
incremental_rows = new_batch_valid[~new_batch_valid["order_id"].isin(history_ids)]

incremental_rows = (
    incremental_rows
    .merge(customers, on="customer_id", how="left")
    .merge(products, on="product_id", how="left")
)
incremental_rows["amount_paid"] = None
incremental_rows["status"] = "pending"
incremental_rows["order_total"] = incremental_rows["quantity"] * incremental_rows["unit_price"]

# Match column order to the existing fact table before appending
incremental_rows = incremental_rows[merged.columns]
incremental_rows.to_sql("fact_orders", conn, if_exists="append", index=False)

print("\nNew batch received:")
print(new_batch)
print("\nRows actually appended (duplicates of history skipped):")
print(incremental_rows)

final_table = pd.read_sql("SELECT * FROM fact_orders", conn)
print("\nFinal fact_orders table after historical + incremental load:")
print(final_table)

conn.close()
print("\nAll tasks complete. Database saved to output/ecommerce_warehouse.db")
