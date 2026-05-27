import requests
import json
import re

headers = {
    "Authorization": "Bearer API-KEY",
    "Content-Type": "application/json",
}

payload = {
    "zone": "serp_api1",
    "url": "https://www.google.com/search?q=site:linkedin.com/jobs/view+software+engineer",
    "format": "json"
}

# SEND REQUEST
response = requests.post(
    "https://api.brightdata.com/request",
    headers=headers,
    json=payload
)

print(response.status_code)

# CONVERT RESPONSE
results = response.json()

# GET HTML BODY
html = results["body"]

# FIND LINKEDIN JOB LINKS
links = re.findall(
    r'https://www\.linkedin\.com/jobs/view/[^"\']+',
    html
)

# REMOVE DUPLICATES
links = list(set(links))

clean_links = []

for link in links:

    # REMOVE TRACKING / TEXT FRAGMENTS
    clean = link.split("#")[0]
    clean = clean.split("%23")[0]

    clean_links.append(clean)

# FINAL UNIQUE LINKS
clean_links = list(set(clean_links))

# RUN ONLY WHEN FILE IS EXECUTED DIRECTLY
if __name__ == "__main__":

    print("\nFOUND JOB LINKS:\n")

    for link in clean_links:
        print(link)