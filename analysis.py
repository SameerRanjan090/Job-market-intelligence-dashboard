import sqlite3
import pandas as pd
from google import genai

# CONNECT DATABASE
conn = sqlite3.connect("jobs.db")

# READ TABLE
df = pd.read_sql_query(
    "SELECT * FROM jobs",
    conn
)


# SHOW DATA
print(df) 

conn.close()
print(df["company"].value_counts().head(10))

print(df["title"].value_counts().head(10))

print(df["location"].value_counts().head(10))

print(df["industry"].value_counts().head(10))

print(df["employment_type"].value_counts())

print(df["experience_level"].value_counts())

print(df["salary"].dropna().head(5))

print(df["skills"].dropna().head(5))

print(df["posted_date"].dropna().head(5))

# AI SUMMARY
API_KEY = "YOUR_API_KEY_HERE"

client = genai.Client(api_key=API_KEY)


prompt = f"""
You are a job market intelligence analyst.

Analyze this dataset and give insights:

Total Jobs: {len(df)}

Top Companies:
{df['company'].value_counts().head(5).to_string()}

Top Job Titles:
{df['title'].value_counts().head(5).to_string()}

Top Locations:
{df['location'].value_counts().head(5).to_string()}

Top Industries:
{df['industry'].value_counts().head(5).to_string()}

Employment Types:
{df['employment_type'].value_counts().to_string()}

Experience Levels:
{df['experience_level'].value_counts().to_string()}

Sample Skills:
{df['skills'].dropna().head(5).to_string()}

Sample Salary Data:
{df['salary'].dropna().head(5).to_string()}

Posted Date Sample:
{df['posted_date'].dropna().head(5).to_string()}

Give a 5–6 line simple job market insight for students and job seekers.
"""


try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    print("\n AI SUMMARY \n")
    print(response.text)

except Exception as e:
    print("\n Gemini Error:")
    print(e)

