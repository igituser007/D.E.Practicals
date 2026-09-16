Data Engineering Lab - Practical Submission
==============================================

PRACTICALS COMPLETED (10 of 10)
----------------------------------
- Practical 01 - Data Handling (parsing TXT/CSV/HTML/XML/JSON + missing
  values/anomalies, binary files, regex, relational DB CRUD)
- Practical 02 - ETL Process to Construct a Database in SQL Server /
  Power BI
- Practical 03 - Handling Missing Values, Duplicate Records, Normalization
- Practical 04 - Noise Elimination, Feature Selection, and EDA
- Practical 05 - Extracting Data from APIs and Flat Files
- Practical 06 - Setting Up Apache Airflow and Creating a DAG
- Practical 07 - ETL Pipeline Design Tasks (6 sub-tasks, one practical)
- Practical 08 - PySpark DataFrame Operations (5 sub-tasks, one practical)
- Practical 09 - End-to-End Data Pipeline (3 sub-tasks, one practical)
- Practical 10 - Mini Project: End-to-End Data Engineering Solution

SOFTWARE / ENVIRONMENT USED
-----------------------------
- Python 3.12
- Java 21 (OpenJDK) - required only for Practical 08 (PySpark)
- SQLite (via Python's built-in sqlite3 module) - used throughout,
  including as a local stand-in wherever SQL Server was specified
  but unavailable (Practical 02)
- Apache Airflow 2.9.3, installed in its OWN virtual environment for
  Practical 06 (see below) so its dependencies don't conflict with the
  other practicals
- SQL Server and Power BI Desktop are referenced in Practical 02 but are
  NOT installed here - see that practical's README for why and what was
  provided instead

INSTALLATION
------------
1. Everything except Practicals 06 and 08:
     pip install -r requirements.txt

2. Practical 06 (Airflow) - install separately in its own environment to
   avoid dependency conflicts:
     cd Practical_06
     python3 -m venv airflow_venv
     ./airflow_venv/bin/pip install apache-airflow==2.9.3

3. Practical 08 (PySpark) also needs a Java 17+ JRE/JDK on your system
   (e.g. `sudo apt install openjdk-17-jre-headless`), in addition to
   `pip install pyspark`.

HOW TO RUN EACH PRACTICAL
----------------------------
Practicals 01, 03, 04, 05, 07, 09, 10:
     cd Practical_0X
     python3 practical_0X.py

Practical 02 - two parts:
     cd Practical_02
     python3 practical_02_etl.py        (runs the real ETL demo)
   practical_02_sqlserver.sql is meant for SSMS against a real SQL
   Server instance; practical_02_powerbi_steps.txt is a written guide
   for Power BI Desktop. Neither runs in this sandbox - see that
   practical's README.

Practical 06 (Airflow) - see the step-by-step commands in
Practical_06/README.txt (it needs AIRFLOW_HOME set and the metadata DB
initialized before a DAG can be tested).

Practical 08 (PySpark):
     cd Practical_08
     python3 practical_08.py

NOTES ON WHAT COULD / COULDN'T BE FULLY EXECUTED
---------------------------------------------------
- Every practical's Python code was actually run, and every output/
  folder contains real, actual console output and generated files
  (CSVs, PNG charts, SQLite/`.db` files) - nothing here is a fabricated
  or "expected" output unless explicitly labeled as such.
- Practical 02 asks for SQL Server and Power BI Desktop specifically -
  both are proprietary, primarily Windows/GUI-based tools that cannot
  run in this Linux sandbox. The correct T-SQL script and Power BI
  steps are provided as-is (for you to run in your own environment),
  and the same ETL logic was additionally run against a local SQLite
  database so there's genuine, real pipeline output to inspect. Full
  details in Practical_02/README.txt.
- Practical 05's live API call hit a shared rate limit on this sandbox's
  network (GitHub's public API), so a small local fallback sample was
  used to still demonstrate the merge/save logic with genuine computed
  output. The real API-calling code is included and works as-is on an
  unrestricted network. Full details in Practical_05/README.txt.
- Practical 06's Airflow DAG was tested with `airflow tasks test`
  (the standard lightweight way to run a single task), rather than the
  full scheduler + webserver, since those require long-running background
  processes. All three tasks completed with status SUCCESS - see
  Practical_06/README.txt.

SUMMARY OF GENERATED OUTPUTS
-------------------------------
Each Practical_0X/output/ folder contains:
- console_output.txt (the real, executed console output)
- any CSVs, databases (.db), or chart images (.png) that practical
  produces (see each practical's own README.txt for specifics)
