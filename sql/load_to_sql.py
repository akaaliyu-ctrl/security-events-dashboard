from pathlib import Path
import sqlite3
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

df = pd.read_csv(DATA_DIR / "security_events_clean.csv", parse_dates=["timestamp"])

conn = sqlite3.connect(DATA_DIR / "security_events.db")
df.to_sql("events", conn, if_exists="replace", index=False)

check = pd.read_sql("SELECT COUNT(*) FROM events", conn)
print("Rows now in the events table:", check.iloc[0, 0])
conn.close()
