from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

# Works on your PC and inside Docker alike
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

st.set_page_config(page_title="Security Events Dashboard", layout="wide")
st.title("Security Events Dashboard")


@st.cache_data  # load once, reuse on every filter click
def load_data():
    conn = sqlite3.connect(DATA_DIR / "security_events.db")
    df = pd.read_sql("SELECT * FROM events", conn, parse_dates=["timestamp"])
    conn.close()
    return df


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
severities = st.sidebar.multiselect(
    "Severity", sorted(df["severity"].unique()), default=sorted(df["severity"].unique())
)
event_types = st.sidebar.multiselect(
    "Event type",
    sorted(df["event_type"].unique()),
    default=sorted(df["event_type"].unique()),
)

min_date, max_date = df["timestamp"].min().date(), df["timestamp"].max().date()
start_date = st.sidebar.date_input(
    "From", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input("To", max_date, min_value=min_date, max_value=max_date)

filtered = df[
    df["severity"].isin(severities)
    & df["event_type"].isin(event_types)
    & (df["timestamp"].dt.date >= start_date)
    & (df["timestamp"].dt.date <= end_date)
]

# ---------- KPI row ----------
c1, c2, c3 = st.columns(3)
c1.metric("Total events", f"{len(filtered):,}")
c2.metric("Critical events", f"{(filtered['severity'] == 'critical').sum():,}")
c3.metric("Unique source IPs", f"{filtered['source_ip'].nunique():,}")

# ---------- Charts ----------
st.subheader("Events over time")
daily = (
    filtered.groupby(filtered["timestamp"].dt.floor("D"))
    .size()
    .reset_index(name="events")
)
st.plotly_chart(px.line(daily, x="timestamp", y="events"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Events by type")
    tc = filtered["event_type"].value_counts().reset_index(name="count")
    st.plotly_chart(px.bar(tc, x="event_type", y="count"), use_container_width=True)
with right:
    st.subheader("Events by severity")
    sc = filtered["severity"].value_counts().reset_index(name="count")
    st.plotly_chart(
        px.pie(sc, names="severity", values="count", hole=0.4), use_container_width=True
    )

st.subheader("Top 10 source IPs")
ti = filtered["source_ip"].value_counts().head(10).reset_index(name="count")
st.plotly_chart(
    px.bar(ti, x="count", y="source_ip", orientation="h"), use_container_width=True
)

st.subheader("Most recent critical events")
recent = filtered[filtered["severity"] == "critical"].sort_values("timestamp").tail(20)
st.dataframe(
    recent[
        ["timestamp", "event_type", "source_ip", "username", "action_taken", "status"]
    ]
)
