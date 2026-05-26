import requests
import json
import sqlite3

# DATABASE CONNECTION
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# API HEADERS
headers = {
    "Authorization: Bearer actual-key",
    "Content-Type": "application/json",
}

# INPUT DATA
data = {
    "input": [
        {
            "url": "https://www.linkedin.com/jobs/view/software-engineer-at-epic-3986111804/?_l=en"
        },
        {
            "url": "https://www.linkedin.com/jobs/view/software-engineer-at-pave-4310512612/"
        }
    ]
}

# API REQUEST
response = requests.post(
    "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true",
    headers=headers,
    json=data
)

print("Status:", response.status_code)

# SPLIT NDJSON RESPONSE
lines = response.text.strip().split("\n")

jobs = []

for line in lines:
    jobs.append(json.loads(line))

# INSERT INTO DATABASE
for job in jobs:

    print("Company:", job.get("company_name"))
    print("Job Title:", job.get("job_title"))
    print("Job ID:", job.get("job_posting_id"))
    print("-------------------")

    if job.get("company_name") is None:
        continue

    cursor.execute(
        """
        INSERT INTO jobs VALUES (?, ?, ?)
        """,
        (
            job.get("company_name"),
            job.get("job_title"),
            job.get("job_posting_id")
        )
    )

    print("Inserted:", job.get("company_name"))

# SAVE DATABASE
conn.commit()
conn.close()

print("All jobs saved!")
