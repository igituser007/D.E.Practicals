Practical 09 - End-to-End Data Pipeline
=========================================

OBJECTIVE
---------
One combined practical covering three related tasks:
1. Build an end-to-end pipeline: CSV -> Python/Pandas -> Data Cleaning ->
   SQL Database -> Report.
2. Build an ETL pipeline for an e-commerce dataset containing customers,
   orders, products, and payments.
3. Design a data pipeline that handles both historical and newly arriving
   data.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas
- sqlite3 (built into Python's standard library)

FILE TO RUN
-----------
practical_09.py

    python3 practical_09.py

WHAT THE CODE DOES
-------------------
1. Generates sample e-commerce CSVs: customers, products, orders, payments
   (with some intentionally invalid orders - a bad product_id and a
   negative quantity - to clean).
2. Cleans and merges them into one fact table, loads it into a SQLite
   database, and produces a "revenue by city" report.
3. Simulates a second batch of "new" orders arriving later, some of which
   duplicate existing (historical) orders. The pipeline only appends the
   genuinely new rows, demonstrating incremental (rather than full-reload)
   loading.

OUTPUT
------
- output/console_output.txt          : full console output (actual,
  executed) for all three tasks.
- output/ecommerce_warehouse.db      : SQLite database with dim_customers,
  dim_products, and fact_orders tables.
- output/revenue_by_city_report.csv  : the aggregated report from task 1.
- data/                               : the sample CSV source files.

NOTES
-----
No special setup required beyond pandas; SQLite is part of Python's
standard library.
