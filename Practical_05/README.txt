Practical 05 - Extracting Data from APIs and Flat Files Using Python
=====================================================================

OBJECTIVE
---------
Fetch user data from a public REST API, clean it, and merge it with a flat
CSV file containing location details.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- pandas, requests



WHAT THE CODE DOES
-------------------
1. Calls a public REST API and normalizes the JSON response into a
   DataFrame (extract_api_data).
2. Creates and reads a flat CSV file of location details
   (extract_csv_data).
3. Merges the two on a shared "id" column and saves the result.


OUTPUT
------
- output/console_output.txt              : actual console output, including
  the real 403 rate-limit error and the fallback path being used.
- output/cleaned_warehouse_profiles.csv   : the merged dataset (from the
  fallback sample, clearly not live API data - see note above).
- locations.csv                            : the flat file created for the
  merge step.


