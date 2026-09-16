Practical 02 - ETL Process to Construct a Database in SQL Server / Power BI
================================================================================

OBJECTIVE
---------
Perform the Extraction, Transformation, and Loading (ETL) process to
construct a data warehouse in SQL Server / Power BI.
(Source reference: BI.pdf, "Practical 2" - Business Intelligence Lab
Manual, University of Mumbai.)

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- For the SQL Server script: Microsoft SQL Server (any recent version)
  and SQL Server Management Studio (SSMS).
- For the Python demonstration: Python 3, pandas (uses SQLite, which is
  built into Python - no extra database server needed).
- For the reporting step: Power BI Desktop (Windows only).

FILES IN THIS FOLDER
----------------------
1. practical_02_sqlserver.sql
   Correct, ready-to-run T-SQL. Creates a Sales_DW database with a star
   schema (DimCustomer, DimProduct, DimDate, FactSales) and loads it
   with sample data. Run this in SSMS against your own SQL Server.

2. practical_02_etl.py
   The SAME extract -> transform -> load logic, actually executed in
   this environment. Since no SQL Server engine is available in this
   sandbox, it loads into a local SQLite file (output/sales_dw.db)
   instead, as a stand-in target with an identical schema. A commented
   block in the script shows exactly what to change to point it at a
   real SQL Server instance via pyodbc.

3. practical_02_powerbi_steps.txt
   The steps you'd follow in Power BI Desktop to connect to the
   warehouse and build a report. Power BI is a Windows GUI application
   with no scripting interface, so this is a written guide rather than
   executable code - see the "WHY THIS PART WASN'T EXECUTED" note
   inside it.

FILE TO RUN
-----------
    python3 practical_02_etl.py

WHAT THE CODE DOES
-------------------
1. EXTRACT: reads a raw sales export (CSV) simulating a source system,
   including one intentionally invalid row (a negative quantity).
2. TRANSFORM: removes the invalid row, computes a derived "revenue"
   column, and reformats the date into the DateKey format the warehouse
   uses (YYYYMMDD, matching the SQL Server script's schema).
3. LOAD: builds the star-schema warehouse (3 dimension tables + 1 fact
   table) and runs an example report query (total revenue by category).

OUTPUT
------
- output/console_output.txt        : full console output of the Python
  ETL run (actual, executed).
- output/sales_dw.db                : the SQLite warehouse (stand-in for
  the real Sales_DW SQL Server database).
- output/revenue_by_category.csv    : the example report's result.
- data/raw_sales_export.csv         : the simulated raw source data.

IMPORTANT - WHAT COULD AND COULDN'T BE ACTUALLY EXECUTED
--------------------------------------------------------------
- practical_02_etl.py: FULLY EXECUTED. All output in output/ is real,
  not fabricated.
- practical_02_sqlserver.sql: CANNOT be executed in this sandbox - there
  is no SQL Server engine available (it's proprietary, primarily
  Windows-based software). The script is correct, standard T-SQL and is
  provided for you to run in your own SSMS; it was not run here.
- practical_02_powerbi_steps.txt: Power BI Desktop is a Windows GUI
  application that cannot be installed or automated in this sandbox.
  The file describes the correct steps and an expected result (clearly
  labeled as such), rather than a fabricated screenshot.
