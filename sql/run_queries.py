from pathlib import Path
import sqlite3
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
conn = sqlite3.connect(DATA_DIR / "security_events.db")

queries = {
    "1. Events by severity": """
        SELECT severity, COUNT(*) AS total
        FROM events
        GROUP BY severity
        ORDER BY total DESC;""",
    "2. Top 10 IPs behind failed logins": """
        SELECT source_ip, COUNT(*) AS failed_attempts
        FROM events
        WHERE event_type = 'failed_login'
        GROUP BY source_ip
        ORDER BY failed_attempts DESC
        LIMIT 10;""",
    "3. Events per day": """
        SELECT DATE(timestamp) AS day, COUNT(*) AS total
        FROM events
        GROUP BY day
        ORDER BY day;""",
    "4. Critical events not yet resolved": """
        SELECT timestamp, event_type, source_ip, username, status
        FROM events
        WHERE severity = 'critical' AND status <> 'resolved'
        ORDER BY timestamp DESC
        LIMIT 20;""",
}

for title, q in queries.items():
    print(f"\n=== {title} ===")
    print(pd.read_sql(q, conn))

conn.close()
