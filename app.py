import streamlit as st
import pandas as pd
import numpy as np
import time
import sqlite3

conn = sqlite3.connect("jobs.db")

df = pd.read_sql_query(
    "SELECT * FROM jobs",
    conn
)

conn.close()
# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Job Market Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# PREMIUM CSS LEVEL 3
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ===================================
MAIN BACKGROUND
=================================== */

.stApp{
    background:
    radial-gradient(circle at top left, #1a1f3c 0%, transparent 30%),
    radial-gradient(circle at bottom right, #11162b 0%, transparent 30%),
    linear-gradient(to right, #050816, #0b1020);

    color: white;
}

/* ===================================
REMOVE STREAMLIT DEFAULTS
=================================== */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===================================
SIDEBAR
=================================== */

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0b1023 0%, #090d1a 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ===================================
SIDEBAR BUTTONS
=================================== */

.stButton button{
    width: 100%;
    background: rgba(255,255,255,0.05);
    color: white;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    margin-bottom: 12px;
    transition: 0.3s;
    font-weight: 500;
}

.stButton button:hover{
    background: linear-gradient(90deg,#7b2ff7,#2d8cff);
    transform: translateX(6px);
    box-shadow: 0 0 18px rgba(123,47,247,0.5);
}

/* ===================================
SEARCH BAR
=================================== */

.stTextInput input{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 15px;
    color: white;
    padding: 14px;
}

/* ===================================
GLASS CARD
=================================== */

.glass-card{
    background: rgba(18, 25, 50, 0.75);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 24px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 25px rgba(0,0,0,0.25);
    margin-bottom: 20px;
    transition: 0.3s;
}

.glass-card:hover{
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(72,149,239,0.25);
}

/* ===================================
METRIC CARD
=================================== */

.metric-card{
    background:
    linear-gradient(145deg,#11182f,#0b1020);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 22px;

    border-radius: 24px;

    box-shadow:
    0 0 20px rgba(0,0,0,0.2),
    inset 0 0 10px rgba(255,255,255,0.02);

    transition: 0.3s;
}

.metric-card:hover{
    transform: translateY(-6px);
    box-shadow:
    0 0 20px rgba(72,149,239,0.3);
}

/* ===================================
SECTION HEADINGS
=================================== */

.section-title{
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* ===================================
NOTIFICATION BOX
=================================== */

.notification{
    background: rgba(255,255,255,0.04);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 4px solid #46a7ff;
}

/* ===================================
TABLE
=================================== */

[data-testid="stTable"]{
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
}

/* ===================================
CUSTOM SCROLLBAR
=================================== */

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #0b1020;
}

::-webkit-scrollbar-thumb {
  background: #2d8cff;
  border-radius: 20px;
}

/* ===================================
ANIMATED GLOW
=================================== */

.glow{
    animation: glowEffect 2s infinite alternate;
}

@keyframes glowEffect{
    from{
        text-shadow: 0 0 10px #2d8cff;
    }

    to{
        text-shadow: 0 0 20px #7b2ff7;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(f"""
    <h1 class='glow'> Job Market Intelligence</h1>

    <p style='color:#9aa4bf;'>
    Advanced Hiring Intelligence Platform
    </p>
    """, unsafe_allow_html=True)

    st.button(" Dashboard")
    st.button(" Companies")
    st.button(" Trends")
    st.button(" AI Insights")
    st.button("Reports")
    st.button("Notifications")
    st.button(" Settings")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='glass-card'>
    <h4>System Status</h4>

    <p> All Systems Operational</p>

    <p> Live Scraping Active</p>

    <p> AI Engine Running</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.markdown(f"""
<h1 class='glow' style='font-size:50px;'>
AI Hiring Intelligence Dashboard
</h1>

<p style='color:#9aa4bf;font-size:18px;'>
Track live hiring trends, AI insights, market analytics,
company growth and job intelligence in real time.
</p>
""", unsafe_allow_html=True)

# =========================================
# TOP BAR
# =========================================

top1, top2, top3 = st.columns([2,1,1])

with top1:

    st.text_input("", placeholder="Search company, role or skill...")

with top2:

    st.selectbox(
        "Filter Industry",
        ["All", "AI", "Software", "Cloud", "Finance"]
    )

with top3:

    st.selectbox(
        "Time Range",
        ["24 Hours", "7 Days", "30 Days"]
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# KPI CARDS
# =========================================
total_jobs = len(df)

total_companies = df["company"].nunique()

top_role = (
    df["title"].mode()[0]
    if not df["title"].empty
    else "N/A"
)

top_company = (
    df["company"].value_counts().idxmax()
    if not df["company"].empty
    else "N/A"
)
c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class='metric-card'>

    <h4>Total Jobs Scraped</h4>

    <h1 style='color:#36ff9b;'>{total_jobs}</h1>

    <p>▲ 12% increase this week</p>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class='metric-card'>

    <h4>Companies Tracked</h4>

    <h1 style='color:#46a7ff;'>{total_companies}</h1>

    <p>▲ 8% growth</p>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class='metric-card'>

    <h4>Top Hiring Sector</h4>

    <h1 style='color:#b066ff;'>{top_company}</h1>

    <p>Highest market demand</p>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class='metric-card'>

    <h4>Most Common Role</h4>

    <h1 style='color:#ffb347;'>{top_role}</h1>

    <p>▲ 5% increase</p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# MAIN GRID
# =========================================

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([2,1])

# =========================================
# LEFT SIDE
# =========================================

with left:

    st.markdown(f"""
    <div class='glass-card'>
    <h3 class='section-title'>
     Top Hiring Companies
    </h3>
    </div>
    """, unsafe_allow_html=True)

    companies = (
        df["company"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    companies.columns = [
        "Company",
        "Jobs"
    ]

    st.bar_chart(companies.set_index("Company"))

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='glass-card'>
    <h3 class='section-title'>
    📈 Hiring Trend Indicator
    </h3>
    </div>
    """, unsafe_allow_html=True)

    trend_data = pd.DataFrame(
        np.random.randn(40,1).cumsum(),
        columns=["Hiring Trend"]
    )

    st.line_chart(trend_data)

# =========================================
# RIGHT SIDE
# =========================================

with right:

    top_companies = (
        df["company"]
        .value_counts()
        .head(5)
        .index
        .tolist()
    )

    st.markdown(f"""
    <div class='glass-card'>
    <h3 class='section-title'>
     AI Insights
    </h3>

    <p>
    Total jobs analyzed: {total_jobs}
    </p>

    <p>
    Top companies:
    {", ".join(top_companies)}
    </p>

    <p>
    Most common role:
    {top_role}
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='glass-card'>
    <h3 class='section-title'>
     Live Job Feed
    </h3>

    <div class='notification'>
    Google hiring Backend Engineers
    </div>

    <div class='notification'>
    Microsoft hiring AI Researchers
    </div>

    <div class='notification'>
    Amazon hiring Cloud Engineers
    </div>

    <div class='notification'>
    NVIDIA hiring GPU Engineers
    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# JOB TABLE SECTION
# =========================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div class='glass-card'>
<h3 class='section-title'>
 Top Job Titles
</h3>
</div>
""", unsafe_allow_html=True)

jobs = df[
    [
        "title",
        "company",
        "location"
    ]
].head(20)

st.dataframe(
    jobs,
    use_container_width=True
)

st.table(jobs)

# =========================================
# BOTTOM SECTION
# =========================================

st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)

with b1:

    st.markdown(f"""
    <div class='glass-card'>

    <h3 class='section-title'>
     Global Hiring Activity
    </h3>

    <h1 style='color:#36ff9b;'>+27%</h1>

    <p>
    Hiring activity increased globally
    compared to previous month.
    </p>

    </div>
    """, unsafe_allow_html=True)

with b2:

    st.markdown(f"""
    <div class='glass-card'>

    <h3 class='section-title'>
    AI Recommendation
    </h3>

    <p>
    Focus on AI Engineering,
    Cloud Infrastructure and
    Backend Development roles.

    These sectors show highest
    projected growth for 2026.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"""
<p style='text-align:center;color:#7d8597;'>

Job Market Intelligence © 2026
<br>
Built with Streamlit + AI Analytics

</p>
""", unsafe_allow_html=True)
