Practical 01 - Data Handling
==============================

OBJECTIVE
---------
Perform various data handling operations using Python:
1. Parse TXT, CSV, HTML, XML and JSON documents, and identify missing
   values and anomalies in each.
2. Read and write binary files.
3. Search, split, and replace strings using regular expressions.
4. Design and populate a relational database and perform CRUD operations
   using SQL.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3 only - every library used (csv, json, re, struct, sqlite3,
  html.parser, xml.etree.ElementTree) is part of Python's standard
  library, so there is nothing extra to install.

FILE TO RUN
-----------
practical_01.py

    python3 practical_01.py

WHAT THE CODE DOES
-------------------
PART 1 - Parsing + missing values/anomalies:
  - TXT:  writes and reads back a plain text file.
  - CSV:  a small students table with one missing "age" and two
          out-of-range values (a negative age, marks over 100) - all
          three are detected and reported.
  - HTML: a small table with one empty cell - detected as missing.
  - XML:  a student record missing its <age> element - detected.
  - JSON: one record missing its "age" field, another with "age" as
          text instead of a number - both detected.

PART 2 - Binary files:
  - Packs a list of integers (plus a 4-byte header) into a binary file
    using the `struct` module, then reads it back and verifies the
    values match exactly.

PART 3 - Regular expressions:
  - Search: finds email addresses and a phone number in sample text.
  - Split: splits the text into sentences.
  - Replace: masks the email addresses with "[EMAIL HIDDEN]".

PART 4 - Relational database + CRUD:
  - Creates a "students" table in SQLite, then performs Create (insert
    3 rows), Read (select all), Update (change one student's marks),
    and Delete (remove one student) - printing the table contents at
    each stage.

OUTPUT
------
- output/console_output.txt : full console output (actual, executed).
- output/console_report.txt : the same run's output, saved separately
  as a plain text report.
- output/numbers.bin         : the binary file from Part 2.
- output/students.db         : the SQLite database from Part 4.
- data/                       : the sample TXT/CSV/HTML/XML/JSON source
  files generated and parsed by Part 1.

NOTES
-----
HTML and XML parsing use Python's built-in html.parser and
xml.etree.ElementTree, rather than third-party libraries (e.g.
BeautifulSoup or lxml), so this practical has zero external
dependencies.
