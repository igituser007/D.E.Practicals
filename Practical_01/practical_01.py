"""
Practical 01: Data Handling
----------------------------
Covers four parts:
  1. Parsing TXT, CSV, HTML, XML, and JSON documents, and identifying
     missing values and anomalies in each.
  2. Reading and writing binary files.
  3. Searching, splitting, and replacing strings using regular expressions.
  4. Designing and populating a relational database and performing CRUD
     operations using SQL.
"""

import os
import re
import csv
import json
import struct
import sqlite3
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

report_lines = []


def log(*args):
    """Print to console AND collect for the saved text report."""
    text = " ".join(str(a) for a in args)
    print(text)
    report_lines.append(text)


# ============================================================
# PART 1: Parsing TXT, CSV, HTML, XML, JSON + finding
#         missing values / anomalies
# ============================================================
log("=" * 60)
log("PART 1: Parsing Different File Formats")
log("=" * 60)

# ---- 1a. TXT ----
with open("data/sample.txt", "w") as f:
    f.write("Data Engineering Lab\nStudent: Prachi\nRoll No: 12\n")

with open("data/sample.txt") as f:
    txt_content = f.read()

log("\n[TXT] Raw content:")
log(txt_content)

# ---- 1b. CSV (with a missing value and an anomaly) ----
with open("data/students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "age", "marks"])
    writer.writerow([1, "Amit", 21, 85])
    writer.writerow([2, "Riya", "", 90])       # missing age
    writer.writerow([3, "Neha", -5, 78])       # anomaly: negative age
    writer.writerow([4, "Karan", 22, 999])     # anomaly: impossible marks

log("\n[CSV] Parsed rows:")
with open("data/students.csv") as f:
    reader = csv.DictReader(f)
    csv_rows = list(reader)
for row in csv_rows:
    log(row)

log("\n[CSV] Missing values / anomalies found:")
for row in csv_rows:
    issues = []
    if row["age"] == "":
        issues.append("missing age")
    elif int(row["age"]) < 0:
        issues.append(f"anomalous age ({row['age']})")
    if int(row["marks"]) > 100:
        issues.append(f"anomalous marks ({row['marks']})")
    if issues:
        log(f"  Row id={row['id']} ({row['name']}): {', '.join(issues)}")

# ---- 1c. HTML (with a missing table cell) ----
html_doc = """
<html><body>
<table>
<tr><td>id</td><td>name</td><td>city</td></tr>
<tr><td>1</td><td>Amit</td><td>Pune</td></tr>
<tr><td>2</td><td>Riya</td><td></td></tr>
</table>
</body></html>
"""
with open("data/sample.html", "w") as f:
    f.write(html_doc)


class TableParser(HTMLParser):
    """A small HTMLParser that pulls table cell text out of simple HTML."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self._current_row = []
        self._in_cell = False
        self._cell_buffer = ""

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag == "td":
            self._in_cell = True
            self._cell_buffer = ""

    def handle_endtag(self, tag):
        if tag == "tr" and self._current_row:
            self.rows.append(self._current_row)
        elif tag == "td":
            # Always record the cell, even if it was empty - otherwise an
            # empty <td></td> would silently shift the row's other columns.
            self._current_row.append(self._cell_buffer.strip())
            self._in_cell = False

    def handle_data(self, data):
        if self._in_cell:
            self._cell_buffer += data


with open("data/sample.html") as f:
    parser = TableParser()
    parser.feed(f.read())

log("\n[HTML] Parsed table rows:")
for row in parser.rows:
    log(row)

log("\n[HTML] Missing values found:")
header, *html_data_rows = parser.rows
for row in html_data_rows:
    for col_name, value in zip(header, row):
        if value == "":
            log(f"  Row {row}: missing '{col_name}'")

# ---- 1d. XML (with a missing element) ----
xml_doc = """<?xml version="1.0"?>
<students>
  <student id="1"><name>Amit</name><age>21</age></student>
  <student id="2"><name>Riya</name></student>
</students>
"""
with open("data/sample.xml", "w") as f:
    f.write(xml_doc)

tree = ET.parse("data/sample.xml")
root = tree.getroot()

log("\n[XML] Parsed students:")
for student in root.findall("student"):
    name = student.find("name").text if student.find("name") is not None else None
    age_elem = student.find("age")
    age = age_elem.text if age_elem is not None else None
    log(f"  id={student.get('id')} name={name} age={age}")
    if age is None:
        log(f"    -> missing 'age' element for student id={student.get('id')}")

# ---- 1e. JSON (with a missing field and a type anomaly) ----
json_data = [
    {"id": 1, "name": "Amit", "age": 21},
    {"id": 2, "name": "Riya"},           # missing "age"
    {"id": 3, "name": "Neha", "age": "twenty"},  # anomaly: age is not a number
]
with open("data/sample.json", "w") as f:
    json.dump(json_data, f, indent=2)

with open("data/sample.json") as f:
    parsed_json = json.load(f)

log("\n[JSON] Parsed records:")
for record in parsed_json:
    log(record)

log("\n[JSON] Missing values / anomalies found:")
for record in parsed_json:
    if "age" not in record:
        log(f"  id={record['id']}: missing 'age' field")
    elif not isinstance(record["age"], int):
        log(f"  id={record['id']}: 'age' has an unexpected type ({record['age']!r})")


# ============================================================
# PART 2: Reading and Writing Binary Files
# ============================================================
log("\n" + "=" * 60)
log("PART 2: Reading and Writing Binary Files")
log("=" * 60)

# Write a small binary file: a header plus a list of integers, packed
# using the 'struct' module (4-byte signed integers, big-endian).
numbers_to_store = [10, 20, 30, 40, 50]

with open("output/numbers.bin", "wb") as f:
    f.write(b"NUMS")  # a 4-byte header/magic string
    for num in numbers_to_store:
        f.write(struct.pack(">i", num))

log(f"\nWrote {len(numbers_to_store)} integers to output/numbers.bin")

# Read it back and verify
with open("output/numbers.bin", "rb") as f:
    header = f.read(4)
    read_numbers = []
    while True:
        chunk = f.read(4)
        if not chunk:
            break
        read_numbers.append(struct.unpack(">i", chunk)[0])

log(f"Header read back: {header}")
log(f"Numbers read back: {read_numbers}")
log(f"Matches what was written: {read_numbers == numbers_to_store}")


# ============================================================
# PART 3: Regular Expressions - Search, Split, Replace
# ============================================================
log("\n" + "=" * 60)
log("PART 3: Regular Expressions")
log("=" * 60)

sample_text = "Contact us at support@example.com or sales@example.org for help. Phone: 9876543210."

# Search: find all email addresses
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", sample_text)
log(f"\nSearch - emails found: {emails}")

# Search: find a 10-digit phone number
phone_match = re.search(r"\b\d{10}\b", sample_text)
log(f"Search - phone number found: {phone_match.group() if phone_match else None}")

# Split: split the text into sentences using '.' as the delimiter
sentences = re.split(r"\.\s*", sample_text)
log(f"\nSplit - sentences: {[s for s in sentences if s]}")

# Replace: mask the email addresses
masked_text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL HIDDEN]", sample_text)
log(f"\nReplace - masked text: {masked_text}")


# ============================================================
# PART 4: Relational Database Design + CRUD Operations
# ============================================================
log("\n" + "=" * 60)
log("PART 4: Relational Database - Design + CRUD")
log("=" * 60)

DB_PATH = "output/students.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- Design: create the table ---
cur.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    marks INTEGER
)
""")
log("\nTable 'students' created.")

# --- Create (Insert) ---
students_to_insert = [
    (1, "Amit", 21, 85),
    (2, "Riya", 22, 90),
    (3, "Neha", 23, 78),
]
cur.executemany("INSERT INTO students (id, name, age, marks) VALUES (?, ?, ?, ?)",
                 students_to_insert)
conn.commit()
log(f"Inserted {len(students_to_insert)} rows (CREATE).")

# --- Read (Select) ---
cur.execute("SELECT * FROM students")
log("\nAll students (READ):")
for row in cur.fetchall():
    log(f"  {row}")

# --- Update ---
cur.execute("UPDATE students SET marks = 95 WHERE name = 'Amit'")
conn.commit()
log("\nUpdated Amit's marks to 95 (UPDATE).")

cur.execute("SELECT * FROM students WHERE name = 'Amit'")
log(f"  After update: {cur.fetchone()}")

# --- Delete ---
cur.execute("DELETE FROM students WHERE name = 'Neha'")
conn.commit()
log("\nDeleted Neha's record (DELETE).")

cur.execute("SELECT * FROM students")
log("\nFinal table contents:")
for row in cur.fetchall():
    log(f"  {row}")

conn.close()

# Save the whole run as a text report too, in addition to the .db file
with open("output/console_report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\nAll parts complete. See output/ for numbers.bin, students.db, and console_report.txt")
