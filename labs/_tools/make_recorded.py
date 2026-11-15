"""Write the recorded replies of Rafiq, the notebook assistant, into labs/data/recorded/.

    uv run python _tools/make_recorded.py

The replies are scripted for the course. Each one carries choices and errors that the sessions teach, and
its code runs for real against the synthetic data. They are not captured from one product or model.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "recorded"
SET = {"temperature": 0.7}
R: dict[str, dict[str, dict]] = {}


def add(lab: str, name: str, request: str, text: str, code: str, context: str = "", settings: dict | None = None) -> None:
    R.setdefault(lab, {})[name] = {"request": request, "context": context, "text": text, "settings": settings or SET,
                                   "code": textwrap.dedent(code).strip()}


# ------------------------------------------------------------------ Lab 1.1
ONE_LINE = "What is our on-time delivery rate?"
add("1.1", "one_line", ONE_LINE,
    "Your on-time delivery rate is 85.3%. I joined deliveries to their delivery scans and averaged the on-time flag.",
    '''
    result = con.sql("""
        SELECT COUNT(*) AS deliveries, AVG(d.on_time_flag) AS on_time_rate
        FROM deliveries d
        JOIN scans s ON s.delivery_id = d.delivery_id
        WHERE s.outcome = 'delivered'
    """).df()
    headline = {"on_time_rate": result.loc[0, "on_time_rate"]}
    ''')

# ------------------------------------------------------------------ Lab 1.3
BRIEF_REQ = "Follow the brief below. Do step 2: the monthly on-time rate."
add("1.3", "brief_v1", BRIEF_REQ,
    "Here is the monthly on-time rate under D-2 for the whole year, without test shipments. One row per month of created_at.",
    '''
    result = con.sql("""
        SELECT strftime(d.created_at, '%Y-%m') AS month,
               COUNT(*) AS deliveries,
               AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1 ELSE 0 END) AS on_time_rate
        FROM deliveries d
        JOIN customers c ON c.customer_id = d.customer_id
        WHERE c.segment <> 'TEST'
        GROUP BY 1 ORDER BY 1
    """).df()
    headline = {"on_time_rate": float((result.on_time_rate * result.deliveries).sum() / result.deliveries.sum())}
    ''')
add("1.3", "brief_v2", "Check 1 failed: the deliveries add up to more than the dispatched parcels. Cancelled orders are in no rate. Fix step 2.",
    "You are right: I had left cancelled orders in the denominator. They are removed now; the total equals the dispatched parcels.",
    '''
    result = con.sql("""
        SELECT strftime(d.created_at, '%Y-%m') AS month,
               COUNT(*) AS deliveries,
               AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1 ELSE 0 END) AS on_time_rate
        FROM deliveries d
        JOIN customers c ON c.customer_id = d.customer_id
        WHERE c.segment <> 'TEST' AND d.status <> 'cancelled'
        GROUP BY 1 ORDER BY 1
    """).df()
    headline = {"on_time_rate": float((result.on_time_rate * result.deliveries).sum() / result.deliveries.sum())}
    ''')

# ------------------------------------------------------------------ Lab 1.4
SHORT = "Monthly on-time rate for Tahani, whole year."
add("1.4", "no_context", SHORT,
    "Here is the monthly on-time rate. I compared each delivery scan with the promised time.",
    '''
    result = con.sql("""
        SELECT strftime(d.created_at, '%Y-%m') AS month,
               COUNT(*) AS deliveries,
               AVG(CASE WHEN s.scan_time_utc <= d.promised_by THEN 1 ELSE 0 END) AS on_time_rate
        FROM deliveries d
        JOIN scans s ON s.delivery_id = d.delivery_id AND s.outcome = 'delivered'
        GROUP BY 1 ORDER BY 1
    """).df()
    headline = {"on_time_rate": float((result.on_time_rate * result.deliveries).sum() / result.deliveries.sum())}
    ''')
add("1.4", "with_context", SHORT,
    "Monthly on-time rate under D-2 for every month of created_at, delivered parcels, test shipments removed, local times.",
    '''
    result = con.sql("""
        WITH base AS (
            SELECT d.*, (d.delivered_at <= d.promised_by) AS ok
            FROM deliveries d
            JOIN customers c ON c.customer_id = d.customer_id
            WHERE c.segment <> 'TEST' AND d.status = 'delivered'
        )
        SELECT strftime(created_at, '%Y-%m') AS month,
               COUNT(*) AS deliveries,
               AVG(CASE WHEN ok THEN 1 ELSE 0 END) AS on_time_rate
        FROM base
        GROUP BY 1 ORDER BY 1
    """).df()
    headline = {"on_time_rate": float((result.on_time_rate * result.deliveries).sum() / result.deliveries.sum())}
    ''', context="the completed AGENTS.md of Lab 1.4")


def main() -> None:
    import importlib
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    for module in ("rec_day2", "rec_day3"):
        if (Path(__file__).resolve().parent / f"{module}.py").exists():
            importlib.import_module(module).register(add)
    OUT.mkdir(parents=True, exist_ok=True)
    for lab, items in R.items():
        path = OUT / f"lab_{lab.replace('.', '_')}.json"
        path.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(path.name, list(items))


if __name__ == "__main__":
    main()
