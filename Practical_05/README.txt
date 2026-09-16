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

FILE TO RUN
-----------
practical_05.py

    python3 practical_05.py

WHAT THE CODE DOES
-------------------
1. Calls a public REST API and normalizes the JSON response into a
   DataFrame (extract_api_data).
2. Creates and reads a flat CSV file of location details
   (extract_csv_data).
3. Merges the two on a shared "id" column and saves the result.

IMPORTANT NOTE ON THE API USED
-------------------------------
The original assignment referenced a placeholder API URL that isn't a real
endpoint. This sandbox also only allows network access to a specific
allow-list of domains, so the script was pointed at GitHub's public REST
API (https://api.github.com/users) instead, since it's a real, live,
reachable public API.

When this was executed, GitHub's anonymous rate limit for this shared
sandbox network was already exhausted (confirmed via a direct curl test,
which returned "API rate limit exceeded"). The script therefore includes
a small fallback sample so the merge/save logic could still be demonstrated
with genuinely computed output. The extraction function itself
(extract_api_data) is real, working code - on a machine/network with a
free API quota (or with a GitHub token added to the request headers), it
will pull live data with no changes needed.

OUTPUT
------
- output/console_output.txt              : actual console output, including
  the real 403 rate-limit error and the fallback path being used.
- output/cleaned_warehouse_profiles.csv   : the merged dataset (from the
  fallback sample, clearly not live API data - see note above).
- locations.csv                            : the flat file created for the
  merge step.

NOTES
-----
If you run this on a network without the API restriction, remove the
"else" fallback block and the request to api.github.com will succeed on
its own.
