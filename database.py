import sqlite3

conn = sqlite3.connect("jobs.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    company TEXT,
    title TEXT,
    job_id TEXT
)
""")

conn.commit()

print("Database and table created!")

conn.close()