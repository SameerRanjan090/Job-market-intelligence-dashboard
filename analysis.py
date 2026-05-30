import sqlite3
import pandas as pd
from google import genai
import streamlit as st


def generate_ai_summary():

    # CONNECT DATABASE
    conn = sqlite3.connect("jobs.db")

    df = pd.read_sql_query(
        "SELECT * FROM jobs",
        conn
    )

    conn.close()

    # CHECK IF DATA EXISTS
    if df.empty:
        return "No job data found."

    # GEMINI CLIENT
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

    # BUILD PROMPT
    prompt = f"""
    You are a job market intelligence analyst.

    Analyze this dataset and give insights.

    Total Jobs:
    {len(df)}

    Top Companies:
    {df['company'].value_counts().head(5).to_string()}

    Top Job Titles:
    {df['title'].value_counts().head(5).to_string()}

    Top Locations:
    {df['location'].value_counts().head(5).to_string()}

    Employment Types:
    {df['employment_type'].value_counts().to_string()}

    Experience Levels:
    {df['experience_level'].value_counts().to_string()}

    Give a short 5-6 line summary for students and job seekers.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {e}"


# RUN DIRECTLY
if __name__ == "__main__":

    summary = generate_ai_summary()

    print("\nAI SUMMARY\n")
    print(summary)
