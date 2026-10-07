# 🛡️ Security Events Dashboard

An end-to-end data project that turns raw security events into an interactive dashboard — covering the full pipeline: **data generation → exploration & cleaning (pandas) → storage & querying (SQLite/SQL) → interactive dashboard (Streamlit + Plotly) → version control (Git) → containerization (Docker)**.

> **Note:** The dataset is a realistic *simulation* of security telemetry (logins, firewall blocks, port scans, malware alerts, privilege escalations), generated with a seeded script so results are reproducible.

## What it does

- Generates **10,000 security events** across 90 days with realistic patterns (attackers reuse IPs, target admin accounts, cluster by country)
- Explores and enriches the data in a Jupyter notebook (trends, top attacker IPs, attack timing)
- Loads everything into a **SQLite** database and answers analyst questions with SQL (top offending IPs, critical unresolved events, daily volumes)
- Serves an **interactive web dashboard** with sidebar filters and live-updating charts

## Dashboard features

- **Filters:** severity, event type, and date range (sidebar)
- **KPIs:** total events, critical events, unique source IPs
- **Charts:** events over time, breakdown by type and severity, top 10 source IPs
- **Table:** most recent critical events for triage

## Tech stack

`Python` · `pandas` · `numpy` · `Plotly` · `Streamlit` · `SQLite` · `Jupyter` · `Git` · `Docker`

## Project structure

```
security-events-dashboard/
├── app/
│   └── dashboard.py          # Streamlit dashboard
├── notebooks/
│   └── 01_explore.ipynb      # Data exploration & cleaning
├── sql/
│   ├── load_to_sql.py        # CSV → SQLite loader
│   └── run_queries.py        # Analyst queries (top IPs, daily volumes, ...)
├── data/                     # Generated data + database (git-ignored)
├── generate_data.py          # Creates the synthetic security events dataset
├── Dockerfile
├── .dockerignore
├── .gitignore
└── requirements.txt
```

## Getting started (Windows, PowerShell)

1. **Clone and enter the project**

   ```powershell
   git clone https://github.com/akaaliyu-ctrl/security-events-dashboard.git
   cd security-events-dashboard
   ```

2. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Generate the dataset and load the database**

   ```powershell
   python generate_data.py
   python sql\load_to_sql.py
   ```

5. **Run the dashboard** — then open http://localhost:8501

   ```powershell
   streamlit run app\dashboard.py
   ```

## Run with Docker

```powershell
docker build -t security-events-dashboard .
docker run -p 8501:8501 security-events-dashboard
```

Then open **http://localhost:8501** in your browser.

## Sample questions the SQL layer answers

```sql
-- Top 10 IPs behind failed login attempts
SELECT source_ip, COUNT(*) AS failed_attempts
FROM events
WHERE event_type = 'failed_login'
GROUP BY source_ip
ORDER BY failed_attempts DESC
LIMIT 10;
```

See `sql/run_queries.py` for more (events per day, critical unresolved events, severity breakdowns).

## Screenshots

<!-- TODO: add a screenshot of the dashboard
     1. Run the app, press Win+Shift+S to capture it
     2. Save as docs/dashboard.png
     3. Replace this comment with: ![dashboard](docs/dashboard.png)
-->

## Author

**akaaliyu-ctrl** — [github.com/akaaliyu-ctrl](https://github.com/akaaliyu-ctrl)
