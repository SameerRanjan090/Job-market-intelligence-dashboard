import requests
import json
import sqlite3
import time

# IMPORT LINKS
from job_finder import clean_links

# DATABASE CONNECTION
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# API HEADERS
headers = {
    "Authorization": "Bearer API-KEY",
    "Content-Type": "application/json"
}

# FORMAT LINKS FOR BRIGHTDATA
job_inputs = []

for link in clean_links:
    job_inputs.append({
        "url": link
    })

print("TOTAL JOBS:", len(job_inputs))

# START SCRAPING
scraper_response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true",
    headers=headers,
    json={
        "input": job_inputs
    }
)

print("SCRAPER STATUS:", scraper_response.status_code)

# SPLIT NDJSON RESPONSE
lines = scraper_response.text.strip().split("\n")

jobs = []

for line in lines:
    jobs.append(json.loads(line))

print("TOTAL JOB RECORDS:", len(jobs))

# SAVE TO DATABASE
for job in jobs:

    company = job.get("company_name")
    title = job.get("job_title")
    job_id = job.get("job_posting_id")

    if company is None:
        continue

    print(company, "-", title)

    cursor.execute(
        """
        INSERT INTO jobs VALUES (?, ?, ?)
        """,
        (
            company,
            title,
            job_id
        )
    )
# SAVE CHANGES
conn.commit()

# CLOSE DATABASE
conn.close()

print("\nALL JOBS SAVED SUCCESSFULLY")
