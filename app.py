#streamlit
import streamlit as st
import sqlite3
import pandas as pd

# PAGE TITLE
st.title("SignalStack AI")

# DATABASE CONNECTION
conn = sqlite3.connect("jobs.db")

# LOAD DATA
df = pd.read_sql_query(
    "SELECT * FROM jobs",
    conn
)

# SHOW DATA
st.write(df)

# SHOW COMPANY COUNTS
st.subheader("Top Hiring Companies")

st.bar_chart(df["company"].value_counts())

conn.close()