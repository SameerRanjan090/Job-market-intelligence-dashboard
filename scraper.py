import requests
import json
import sqlite3
import streamlit as st

# IMPORT LINKS
from job_finder import get_job_links

# GET JOB LINKS
clean_links = get_job_links()

# DATABASE CONNECTION
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# API HEADERS
headers = {
    "Authorization": f"Bearer {st.secrets['BRIGHTDATA_TOKEN']}",
    "Content-Type": "application/json"
}

# FORMAT LINKS FOR BRIGHTDATA
job_inputs = []

for link in clean_links:
    job_inputs.append({
        "url": link
    })

print("TOTAL JOBS:", len(job_inputs))

# STOP IF NO JOBS FOUND
if len(job_inputs) == 0:
    print("No job links found.")
    conn.close()
    exit()

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

    if line.strip():
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

    location = job.get("job_location")
    employment_type = job.get("employment_type")
    experience_level = job.get("seniority_level")
    salary = job.get("salary")
    posted_date = job.get("posted_date")
    job_url = job.get("url")

    cursor.execute(
        """
        INSERT OR IGNORE INTO jobs
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            company,
            title,
            location,
            employment_type,
            experience_level,
            salary,
            None,           # skills
            posted_date,
            None,           # applicants
            None,           # industry
            job_url,
            json.dumps(job)
        )
    )

# SAVE CHANGES
conn.commit()

# CLOSE DATABASE
conn.close()

print("\nALL JOBS SAVED SUCCESSFULLY")
