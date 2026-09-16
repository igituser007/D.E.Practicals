Practical 07 - ETL Pipeline Design Tasks
==========================================

OBJECTIVE
---------
One combined practical covering six ETL design tasks:
1. Extract from a CSV, clean, transform, and store it in a database.
2. Extract data from multiple CSV files and combine them.
3. Extract JSON data, transform selected fields, and load into a database.
4. Identify and remove invalid records.
5. Validate data before loading into the target database.
6. Implement incremental data loading instead of reloading everything.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas
- sqlite3 (built into Python's standard library)

FILE TO RUN
-----------
practical_07.py

    python3 practical_07.py

WHAT THE CODE DOES
-------------------
Each task builds its own small sample dataset (so it's self-contained and
repeatable), then demonstrates the requested behavior:
- Task 1: cleans a sales CSV (drops missing product, fixes missing/negative
  quantity), transforms it (adds a "total" column), loads it into
  a SQLite table called "sales".
- Task 2: combines two separate regional sales CSVs into one DataFrame.
- Task 3: reads a JSON file of customers, keeps only the needed fields,
  loads into a "customers" table.
- Task 4: flags records with a bad email or an out-of-range age as invalid.
- Task 5: re-validates the "valid" records with a stricter check before
  loading into a "validated_customers" table.
- Task 6: loads a "day 1" batch of transactions, then simulates a "day 2"
  batch and appends only the rows that aren't already present (incremental
  load), rather than reloading the whole table.

OUTPUT
------
- output/console_output.txt : full console output (actual, executed) for
  all six tasks.
- output/etl_practical.db   : SQLite database containing all tables created
  across the six tasks (sales, combined_sales, customers,
  validated_customers, transactions).
- data/                      : the sample CSV/JSON source files generated
  and used by the script.

NOTES
-----
No special setup required beyond pandas; SQLite is part of Python's
standard library.
