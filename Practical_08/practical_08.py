"""
Practical 08: PySpark DataFrame Operations
---------------------------------------
A single combined practical covering five PySpark tasks:
  1. Read a CSV dataset and display its schema
  2. Filtering, grouping, and aggregation
  3. Remove duplicate records
  4. Join between two datasets
  5. Calculate average sales by product category
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

os.makedirs("data", exist_ok=True)

spark = SparkSession.builder \
    .appName("Practical08_PySpark") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")  # keep console output readable

# -----------------------------
# Sample sales dataset (CSV)
# -----------------------------
sales_csv = """order_id,category,product,quantity,sales_amount
1,Stationery,Pen,10,100
2,Stationery,Notebook,5,200
3,Electronics,USB Drive,3,900
4,Electronics,Mouse,7,1400
5,Stationery,Pen,10,100
6,Grocery,Rice,20,1000
7,Electronics,Mouse,2,400
8,Grocery,Wheat,15,750
"""
with open("data/sales.csv", "w") as f:
    f.write(sales_csv)

print("=" * 60)
print("TASK 1: Read CSV and Display Schema")
print("=" * 60)

df = spark.read.csv("data/sales.csv", header=True, inferSchema=True)
df.printSchema()
df.show()


print("=" * 60)
print("TASK 2: Filtering, Grouping, and Aggregation")
print("=" * 60)

print("\nFilter: orders with sales_amount > 500")
df.filter(F.col("sales_amount") > 500).show()

print("Group + Aggregate: total sales_amount per category")
df.groupBy("category").agg(F.sum("sales_amount").alias("total_sales")).show()


print("=" * 60)
print("TASK 3: Remove Duplicate Records")
print("=" * 60)

print("\nBefore removing duplicates:")
df.show()

df_no_dupes = df.dropDuplicates(["category", "product", "quantity", "sales_amount"])
print("After removing duplicates (order_id 1 and 5 were identical apart from id):")
df_no_dupes.show()


print("=" * 60)
print("TASK 4: Join Between Two Datasets")
print("=" * 60)

categories_data = [("Stationery", "Aisle 1"), ("Electronics", "Aisle 2"), ("Grocery", "Aisle 3")]
categories_df = spark.createDataFrame(categories_data, ["category", "aisle_location"])

joined_df = df_no_dupes.join(categories_df, on="category", how="inner")
print("\nJoined dataset (sales + aisle location):")
joined_df.show()


print("=" * 60)
print("TASK 5: Average Sales by Product Category")
print("=" * 60)

avg_sales_df = df_no_dupes.groupBy("category").agg(
    F.avg("sales_amount").alias("avg_sales_amount")
).orderBy("category")
avg_sales_df.show()

# Save results for the output folder
avg_sales_df.toPandas().to_csv("output/avg_sales_by_category.csv", index=False)
joined_df.toPandas().to_csv("output/joined_sales_with_location.csv", index=False)

print("Saved avg_sales_by_category.csv and joined_sales_with_location.csv to output/")

spark.stop()
