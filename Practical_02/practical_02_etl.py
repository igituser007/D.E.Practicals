"""
Practical 02: ETL Process - Python Implementation
--------------------------------------------------
Demonstrates the same Extract -> Transform -> Load pipeline as
practical_02_sqlserver.sql, actually executed here so there is genuine,
real output to inspect.

IMPORTANT - target database used:
This sandbox has no SQL Server engine available (it's a Windows-oriented,
proprietary database server - see README.txt), so this script loads into
a local SQLite database (output/sales_dw.db) instead, as a stand-in
target with the exact same schema and logic. The SQL Server version of
this same ETL is provided separately in practical_02_sqlserver.sql, and
a commented-out pyodbc connection block below shows exactly what would
change to point this script at a real SQL Server instance.
"""

import os
import sqlite3
import pandas as pd

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)
DB_PATH = "output/sales_dw.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# ------------------------------------------------------------------
# To point this script at a REAL SQL Server instance instead of the
# local SQLite file above, you would replace the sqlite3.connect(...)
# call below with something like this (requires: pip install pyodbc):
#
#   import pyodbc
#   conn = pyodbc.connect(
#       "DRIVER={ODBC Driver 17 for SQL Server};"
#       "SERVER=your_server_name;"
#       "DATABASE=Sales_DW;"
#       "Trusted_Connection=yes;"
#   )
#
# Everything else in this script (the extract/transform/load logic)
# stays the same either way.
# ------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 60)
print("STEP 1: EXTRACTION - reading raw source data")
print("=" * 60)

# Simulate a "source system" export (this is what a real extraction
# from Excel/Oracle/another database would land as - a raw CSV)
raw_csv = """customer_name,city,product_name,category,sale_date,quantity,unit_price
Riya,Pune,Pen,Stationery,2026-01-05,10,10.00
Amit,Mumbai,Notebook,Stationery,2026-01-05,5,40.00
Neha,Pune,Mouse,Electronics,2026-02-10,2,700.00
Riya,Pune,Notebook,Stationery,2026-02-10,-3,40.00
"""
with open("data/raw_sales_export.csv", "w") as f:
    f.write(raw_csv)

raw_df = pd.read_csv("data/raw_sales_export.csv")
print("\nRaw extracted data:")
print(raw_df)


print("\n" + "=" * 60)
print("STEP 2: TRANSFORMATION - cleaning and shaping for the warehouse")
print("=" * 60)

# Data has to be cleaned before loading: remove rows with a
# non-positive quantity (a bad record from the source system)
clean_df = raw_df[raw_df["quantity"] > 0].copy()

# Derived/calculated column, as required by the target schema
clean_df["revenue"] = clean_df["quantity"] * clean_df["unit_price"]

# Standardize the date into the DateKey format the warehouse expects
# (matches DimDate.DateKey in practical_02_sqlserver.sql: YYYYMMDD)
clean_df["date_key"] = pd.to_datetime(clean_df["sale_date"]).dt.strftime("%Y%m%d").astype(int)

print(f"\nRemoved {len(raw_df) - len(clean_df)} invalid row(s) (non-positive quantity).")
print("\nTransformed data:")
print(clean_df)


print("\n" + "=" * 60)
print("STEP 3: LOADING - building the star-schema warehouse")
print("=" * 60)

# --- Dimension: Customer ---
dim_customer = clean_df[["customer_name", "city"]].drop_duplicates().reset_index(drop=True)
dim_customer.index.name = "customer_key"
dim_customer = dim_customer.reset_index()
dim_customer.to_sql("DimCustomer", conn, if_exists="replace", index=False)

# --- Dimension: Product ---
dim_product = clean_df[["product_name", "category"]].drop_duplicates().reset_index(drop=True)
dim_product.index.name = "product_key"
dim_product = dim_product.reset_index()
dim_product.to_sql("DimProduct", conn, if_exists="replace", index=False)

# --- Dimension: Date ---
dim_date = clean_df[["date_key", "sale_date"]].drop_duplicates().reset_index(drop=True)
dim_date.to_sql("DimDate", conn, if_exists="replace", index=False)

# --- Fact table: linked to the dimensions via keys ---
fact_sales = (
    clean_df
    .merge(dim_customer, on=["customer_name", "city"])
    .merge(dim_product, on=["product_name", "category"])
)[["customer_key", "product_key", "date_key", "quantity", "unit_price", "revenue"]]
fact_sales.to_sql("FactSales", conn, if_exists="replace", index=False)

print("\nWarehouse tables created: DimCustomer, DimProduct, DimDate, FactSales")
print("\nDimProduct:")
print(dim_product)
print("\nFactSales:")
print(fact_sales)


print("\n" + "=" * 60)
print("STEP 4: Example report - total revenue by product category")
print("=" * 60)

report = pd.read_sql("""
    SELECT p.category, SUM(f.revenue) AS total_revenue
    FROM FactSales f
    JOIN DimProduct p ON f.product_key = p.product_key
    GROUP BY p.category
    ORDER BY total_revenue DESC
""", conn)
print("\n", report)
report.to_csv("output/revenue_by_category.csv", index=False)

conn.close()
print("\nAll steps complete. Warehouse saved to output/sales_dw.db")
