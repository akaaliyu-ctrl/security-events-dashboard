"""Generate a realistic sample dataset of security events.

Run from the project root:  python generate_data.py
Creates:                    data/security_events.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)  # fixed seed = same "random" data every run

n = 10_000

# Timestamps spread across the last 90 days
end = pd.Timestamp.now().floor("D")
offsets = rng.integers(0, 90 * 24 * 60 * 60, n)
timestamps = end - pd.to_timedelta(offsets, unit="s")

# Event types with realistic proportions
event_types = [
    "successful_login",
    "failed_login",
    "firewall_block",
    "port_scan",
    "malware_alert",
    "privilege_escalation",
]
types = rng.choice(event_types, n, p=[0.45, 0.25, 0.15, 0.07, 0.05, 0.03])

# Severity depends on the event type (a login is rarely critical,
# privilege escalation almost always is)
severity_map = {
    "successful_login": ["low", "low", "low", "medium"],
    "failed_login": ["low", "medium", "medium", "high"],
    "firewall_block": ["medium", "medium", "high"],
    "port_scan": ["medium", "high"],
    "malware_alert": ["high", "critical", "critical"],
    "privilege_escalation": ["critical", "critical", "high"],
}
severities = [rng.choice(severity_map[t]) for t in types]

# People, machines, and attacker infrastructure
people = ["asmith", "bjones", "clee", "dpatel", "emartin", "fnguyen", "garcia", "hkim"]
attack_targets = ["admin", "root", "administrator", "svc_backup", "test"]
hosts = [f"WS-{i:03d}" for i in range(1, 41)] + [f"SRV-{i:02d}" for i in range(1, 9)]
# 203.0.113.x / 198.51.100.x are IP ranges reserved for documentation,
# so we never accidentally implicate a real server
external = {
    "203.0.113": "Brazil",
    "198.51.100": "Russia",
    "45.33.32": "USA",
    "185.220.101": "Netherlands",
}

ips, countries, users, host_names, actions, statuses = [], [], [], [], [], []
action_map = {
    "successful_login": "allowed",
    "failed_login": "logged",
    "firewall_block": "blocked",
    "port_scan": "alerted",
    "malware_alert": "quarantined",
    "privilege_escalation": "locked_out",
}

for t, sev in zip(types, severities):
    if rng.random() < 0.6:  # 60% internal traffic
        ips.append(f"10.1.{rng.integers(1, 20)}.{rng.integers(2, 250)}")
        countries.append("Internal")
    else:  # 40% external
        prefix = rng.choice(list(external))
        ips.append(f"{prefix}.{rng.integers(1, 254)}")
        countries.append(external[prefix])

    if t in ("failed_login", "privilege_escalation") and rng.random() < 0.7:
        users.append(rng.choice(attack_targets))  # attackers probe admin accounts
    elif t == "successful_login":
        users.append(rng.choice(people))
    else:
        users.append(rng.choice(people) if rng.random() < 0.5 else "-")

    host_names.append(rng.choice(hosts))
    actions.append(action_map[t])
    statuses.append(
        rng.choice(["resolved", "resolved", "investigating", "open"])
        if sev in ("high", "critical")
        else "resolved"
    )

df = (
    pd.DataFrame(
        {
            "timestamp": timestamps,
            "event_type": types,
            "severity": severities,
            "source_ip": ips,
            "country": countries,
            "username": users,
            "host": host_names,
            "action_taken": actions,
            "status": statuses,
        }
    )
    .sort_values("timestamp")
    .reset_index(drop=True)
)
df.insert(0, "event_id", range(1, len(df) + 1))

Path(__file__).parent.joinpath("data").mkdir(exist_ok=True)
df.to_csv(Path(__file__).parent / "data" / "security_events.csv", index=False)

print("Saved", len(df), "events to data/security_events.csv")
print("\nEvents by type:")
print(df["event_type"].value_counts())
print("\nFirst 5 rows:")
print(df.head())
