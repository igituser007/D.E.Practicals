Practical 10 - Mini Project: End-to-End Data Engineering Solution
====================================================================

OBJECTIVE
---------
Design and implement an end-to-end data engineering solution including
data ingestion, cleaning, transformation, storage, data warehouse design,
and reporting.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas, matplotlib
- sqlite3 (built into Python's standard library)

FILE TO RUN
-----------
practical_10.py

    python3 practical_10.py

WHAT THE CODE DOES
-------------------
A small, complete pipeline for a fictional retail store, built in six
stages:

1. INGESTION     - reads raw sales transactions (CSV) and customer info
                    (JSON), including deliberately messy data (duplicates,
                    a missing quantity, a negative quantity, a missing
                    customer name) to clean later.
2. CLEANING      - drops duplicate sales, fills/removes invalid quantities,
                    fills missing customer names with "Unknown".
3. TRANSFORMATION - parses dates, derives a "sale_month" column and a
                    "revenue" column (quantity x unit_price).
4. STORAGE        - loads everything into a SQLite database.
5. WAREHOUSE      - organizes the data into a simple star schema:
                    dim_customers, dim_products (dimensions) and
                    fact_sales (fact table), linked by keys.
6. REPORTING      - runs SQL queries against the warehouse to produce a
                    "revenue by city and category" report and a "revenue
                    by month" report, and saves two bar charts.

OUTPUT
------
- output/console_output.txt              : full console output (actual,
  executed) for all six stages.
- output/retail_warehouse.db              : SQLite data warehouse
  (dim_customers, dim_products, fact_sales tables).
- output/revenue_by_city_category.csv     : report from Stage 6.
- output/monthly_revenue.csv              : report from Stage 6.
- output/monthly_revenue_chart.png        : bar chart of revenue by month.
- output/category_revenue_chart.png       : bar chart of revenue by
  category.
- data/                                    : the raw source files
  (sales.csv, customers.json).

NOTES
-----
Kept deliberately small and readable (a handful of customers/products)
so the full pipeline - and the effect of each cleaning/transformation
step - is easy to follow end to end. The same structure scales to a
larger dataset without changing the approach.
