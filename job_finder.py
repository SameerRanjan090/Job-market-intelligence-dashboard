import requests
import re
import streamlit as st


def get_job_links():

    headers = {
        "Authorization": f"Bearer {st.secrets['BRIGHTDATA_TOKEN']}",
        "Content-Type": "application/json"
    }

    payload = {
        "zone": "serp_api1",
        "url": "https://www.google.com/search?q=site:linkedin.com/jobs/view+software+engineer",
        "format": "json"
    }

    response = requests.post(
        "https://api.brightdata.com/request",
        headers=headers,
        json=payload
    )

    results = response.json()

    html = results["body"]

    links = re.findall(
        r'https://www\.linkedin\.com/jobs/view/[^"\']+',
        html
    )

    links = list(set(links))

    clean_links = []

    for link in links:

        clean = link.split("#")[0]
        clean = clean.split("%23")[0]

        clean_links.append(clean)

    clean_links = list(set(clean_links))

    return clean_links


if __name__ == "__main__":

    links = get_job_links()

    print("\nFOUND JOB LINKS:\n")

    for link in links:
        print(link)
