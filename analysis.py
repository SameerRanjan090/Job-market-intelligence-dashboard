import sqlite3
import pandas as pd

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
print(df["company"].value_counts())
print(df["title"].value_counts())