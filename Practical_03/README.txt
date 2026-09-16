Practical 03 - Handling Missing Values, Duplicate Records, and Data Normalization
================================================================================

OBJECTIVE
---------
Use Pandas to clean a small dataset: fill missing values, remove duplicate
rows, and normalize numeric columns using min-max scaling.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas

FILE TO RUN
-----------
practical_03.py

    python3 practical_03.py

WHAT THE CODE DOES
-------------------
1. Builds a small sample DataFrame with missing Name/Age/Marks values and
   one duplicate row.
2. Fills missing Age and Marks with the column mean, and missing Name with
   "Unknown".
3. Drops duplicate rows.
4. Normalizes Age and Marks to a 0-1 range using min-max normalization.

OUTPUT
------
- output/console_output.txt : full console output of the run (actual, not
  expected - this was executed).
- output/cleaned_data.csv   : the final cleaned + normalized dataset.

NOTES
-----
No special setup required; this practical runs anywhere pandas is installed.
