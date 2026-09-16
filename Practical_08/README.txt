Practical 08 - PySpark DataFrame Operations
==============================================

OBJECTIVE
---------
One combined practical covering five PySpark tasks:
1. Read a CSV dataset and display its schema.
2. Filtering, grouping, and aggregation.
3. Remove duplicate records.
4. Join between two datasets.
5. Calculate average sales by product category.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- Java (JDK/JRE 17+) - required by Spark
- pyspark

FILE TO RUN
-----------
practical_08.py

    python3 practical_08.py

WHAT THE CODE DOES
-------------------
Starts a local Spark session, writes a small sample sales CSV, then:
1. Reads it back and prints the inferred schema + full contents.
2. Filters rows above a sales threshold and aggregates total sales per
   category.
3. Removes duplicate rows (two orders were identical apart from order_id).
4. Joins the sales data against a small "category -> aisle location"
   lookup table.
5. Computes average sales amount per category.

OUTPUT
------
- output/console_output.txt              : full console output (actual,
  executed - a real local Spark session ran this).
- output/avg_sales_by_category.csv        : result of task 5.
- output/joined_sales_with_location.csv   : result of task 4.

NOTES
-----
Runs Spark in local mode (`.master("local[*]")`) so no cluster is needed.
You may see harmless warnings about PyArrow/pandas version compatibility
in the console output - these don't affect the results, Spark falls back
to a non-Arrow code path automatically.
