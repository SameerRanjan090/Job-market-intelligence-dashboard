import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    company TEXT,
    title TEXT,
    location TEXT,
    employment_type TEXT,
    experience_level TEXT,
    salary TEXT,
    skills TEXT,
    posted_date TEXT,
    applicants INTEGER,
    industry TEXT,
    job_url TEXT,
    raw_json TEXT
)
""")

conn.commit()

print("Database is ready!")

conn.close()
