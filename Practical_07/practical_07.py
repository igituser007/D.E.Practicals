"""
Practical 07: ETL Pipeline Design Tasks
------------------------------------
A single combined practical covering six ETL design tasks:
  1. Extract from a CSV, clean, transform, and store it in a database
  2. Extract data from multiple CSV files and combine them
  3. Extract JSON data, transform selected fields, and load into a database
  4. Identify and remove invalid records
  5. Validate data before loading into the target database
  6. Implement incremental data loading instead of reloading everything
"""

import os
import json
import sqlite3
import pandas as pd

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)
DB_PATH = "output/etl_practical.db"

# Start with a clean database each run so the demo is repeatable
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("TASK 1: Extract from CSV -> Clean -> Transform -> Store in DB")
print("=" * 60)

# Create a sample "sales" CSV to extract from
sales_data = {
    "order_id": [1, 2, 3, 4, 5],
    "product": ["Pen", "Notebook", "Pen", None, "Eraser"],
    "quantity": [10, 5, -2, 3, None],
    "price": [10.0, 40.0, 10.0, 25.0, 5.0],
}
pd.DataFrame(sales_data).to_csv("data/sales.csv", index=False)

df_sales = pd.read_csv("data/sales.csv")
print("\nExtracted:")
print(df_sales)

# Clean: drop rows with missing product, fill missing quantity with 0,
# and remove clearly invalid (negative) quantities
df_sales_clean = df_sales.dropna(subset=["product"]).copy()
df_sales_clean["quantity"] = df_sales_clean["quantity"].fillna(0)
df_sales_clean = df_sales_clean[df_sales_clean["quantity"] >= 0]

# Transform: add a computed "total" column
df_sales_clean["total"] = df_sales_clean["quantity"] * df_sales_clean["price"]

print("\nCleaned & Transformed:")
print(df_sales_clean)

df_sales_clean.to_sql("sales", conn, if_exists="replace", index=False)
print("\nStored in database table 'sales'.")


print("\n" + "=" * 60)
print("TASK 2: Extract from Multiple CSVs and Combine")
print("=" * 60)

pd.DataFrame({"order_id": [6, 7], "product": ["Ruler", "Sharpener"],
              "quantity": [4, 8], "price": [15.0, 8.0]}).to_csv("data/sales_region_a.csv", index=False)
pd.DataFrame({"order_id": [8, 9], "product": ["Pencil", "Glue"],
              "quantity": [12, 2], "price": [5.0, 30.0]}).to_csv("data/sales_region_b.csv", index=False)

csv_files = ["data/sales_region_a.csv", "data/sales_region_b.csv"]
combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
print("\nCombined dataset from multiple CSVs:")
print(combined_df)
combined_df.to_sql("combined_sales", conn, if_exists="replace", index=False)


print("\n" + "=" * 60)
print("TASK 3: Extract JSON -> Transform Selected Fields -> Load to DB")
print("=" * 60)

json_data = [
    {"customer_id": 1, "name": "Aman", "city": "Pune", "signup_year": 2023, "extra_field": "ignore_me"},
    {"customer_id": 2, "name": "Sara", "city": "Mumbai", "signup_year": 2024, "extra_field": "ignore_me"},
]
with open("data/customers.json", "w") as f:
    json.dump(json_data, f)

with open("data/customers.json") as f:
    raw_json = json.load(f)

df_customers = pd.json_normalize(raw_json)
# Transform: keep only the selected fields we care about
df_customers = df_customers[["customer_id", "name", "city", "signup_year"]]
print("\nSelected fields from JSON:")
print(df_customers)

df_customers.to_sql("customers", conn, if_exists="replace", index=False)
print("\nStored in database table 'customers'.")


print("\n" + "=" * 60)
print("TASK 4: Identify and Remove Invalid Records")
print("=" * 60)

raw_records = pd.DataFrame({
    "record_id": [1, 2, 3, 4, 5],
    "email": ["a@test.com", "not-an-email", "b@test.com", "", "c@test.com"],
    "age": [25, -5, 40, 30, 200],
})
print("\nRaw records:")
print(raw_records)

valid_mask = (
    raw_records["email"].str.contains("@", na=False)
    & (raw_records["age"] > 0)
    & (raw_records["age"] < 120)
)
invalid_records = raw_records[~valid_mask]
valid_records = raw_records[valid_mask]

print("\nInvalid records identified (bad email or out-of-range age):")
print(invalid_records)
print("\nValid records kept:")
print(valid_records)


print("\n" + "=" * 60)
print("TASK 5: Validate Data Before Loading into Target Database")
print("=" * 60)


def validate_row(row):
    """Return True only if the row passes all basic sanity checks."""
    return (
        pd.notna(row["email"])
        and "@" in str(row["email"])
        and 0 < row["age"] < 120
    )


rows_to_load = valid_records[valid_records.apply(validate_row, axis=1)]
rows_to_load.to_sql("validated_customers", conn, if_exists="replace", index=False)
print(f"\n{len(rows_to_load)} of {len(raw_records)} rows passed validation and were loaded.")


print("\n" + "=" * 60)
print("TASK 6: Incremental Data Loading")
print("=" * 60)

# Simulate "day 1" load
day1 = pd.DataFrame({"txn_id": [101, 102, 103], "amount": [500, 750, 300]})
day1.to_sql("transactions", conn, if_exists="replace", index=False)
print("\nDay 1 load (full load):")
print(pd.read_sql("SELECT * FROM transactions", conn))

# Simulate "day 2": only NEW rows arrive, append instead of reloading everything
day2_new_rows = pd.DataFrame({"txn_id": [104, 105], "amount": [620, 410]})

existing_ids = pd.read_sql("SELECT txn_id FROM transactions", conn)["txn_id"].tolist()
incremental_rows = day2_new_rows[~day2_new_rows["txn_id"].isin(existing_ids)]
incremental_rows.to_sql("transactions", conn, if_exists="append", index=False)

print("\nDay 2 incremental load (only new rows appended):")
print(pd.read_sql("SELECT * FROM transactions", conn))

conn.close()
print("\nAll tasks complete. Database saved to output/etl_practical.db")
