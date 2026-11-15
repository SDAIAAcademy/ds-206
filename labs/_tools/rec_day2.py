"""Recorded replies of Day 2 (scripted for the course; see make_recorded.py)."""

FIVE = ("Since July 2026, which city has the worst on-time performance, and which cities got worse than before July? "
        "Set result to one row per city with the columns city, before, since and worse, and headline to worst_city and measure.")
SET5 = {"temperature": 0.7, "top_p": 1.0}

BY_CITY = '''
result = con.sql("""
    SELECT d.city,
           AVG(CASE WHEN d.created_at <  DATE '2026-07-01' THEN {ok} END) AS before,
           AVG(CASE WHEN d.created_at >= DATE '2026-07-01' THEN {ok} END) AS since
    FROM deliveries d
    JOIN customers c ON c.customer_id = d.customer_id
    WHERE c.segment <> 'TEST' AND {keep}
    GROUP BY d.city ORDER BY d.city
""").df()
result["worse"] = result.since < result.before - {margin}
headline = {{"worst_city": result.sort_values("since").city.iloc[0], "measure": "{measure}"}}
'''
D2 = "CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END"


def register(add) -> None:
    # -------------------------------------------------------------- Lab 2.1
    add("2.1", "dammam_quarters", "On-time rate for Dammam by quarter. Did the third quarter of 2026 get worse?",
        "Dammam is steady: about 87% on time in every quarter, with a dip of under three points in the third quarter of 2026. "
        "I matched each parcel to its delivery scan in pandas and compared the scan time with the promised time.",
        '''
        d = con.sql("SELECT delivery_id, promised_by FROM deliveries WHERE city = 'Dammam'").df()
        s = con.sql("SELECT delivery_id, scan_time_utc FROM scans WHERE outcome = 'delivered'").df()
        m = d.merge(s, on="delivery_id")
        m["quarter"] = m.scan_time_utc.dt.to_period("Q").astype(str)
        m["ok"] = m.scan_time_utc <= m.promised_by
        result = (m.groupby("quarter").agg(deliveries=("delivery_id", "size"), on_time_rate=("ok", "mean"))
                   .reset_index().query("quarter <= '2026Q3'"))
        headline = {"q2_2026": result.set_index("quarter").on_time_rate["2026Q2"],
                    "q3_2026": result.set_index("quarter").on_time_rate["2026Q3"]}
        ''')

    # -------------------------------------------------------------- Lab 2.2
    add("2.2", "long_routes", "Dammam, July to September 2026: are parcels on long routes (more than 60 planned stops) on time less often?",
        "Yes: 70.3% of parcels on long routes are on time against 81.4% on the others. I joined each parcel to its route plan and its driver's shift, "
        "kept full shifts, and compared routes above 60 planned stops with the rest.",
        '''
        result = con.sql("""
            WITH j AS (
                SELECT d.delivery_id,
                       p.planned_stops > 60 AS long_route,
                       d.delivered_at <= d.promised_by AS ok
                FROM deliveries d
                JOIN customers c ON c.customer_id = d.customer_id
                JOIN route_plans p
                  ON p.hub_id = d.hub_id AND p.plan_date = d.route_date AND p.route_id = d.route_id
                LEFT JOIN driver_shifts s
                  ON s.driver_id = d.driver_id AND s.shift_date = d.route_date
                WHERE d.city = 'Dammam'
                  AND c.segment <> 'TEST'
                  AND d.created_at BETWEEN '2026-07-01' AND '2026-09-30'
                  AND d.status = 'delivered'
                  AND s.hours >= 8
            )
            SELECT long_route, COUNT(*) AS parcels, AVG(CASE WHEN ok THEN 1.0 ELSE 0.0 END) AS on_time_rate
            FROM j GROUP BY long_route ORDER BY long_route
        """).df()
        headline = {"short": result.on_time_rate[0], "long": result.on_time_rate[1], "parcels": int(result.parcels.sum())}
        ''')

    # -------------------------------------------------------------- Lab 2.3
    add("2.3", "chart", "Chart late deliveries since July for Riyadh and Dammam.",
        "Here is the weekly chart. Riyadh has far more late deliveries than Dammam, and both fall sharply in the last week.",
        '''
        result = con.sql("""
            SELECT CAST(date_trunc('week', d.created_at) AS DATE) AS week, d.city, COUNT(*) AS late_deliveries
            FROM deliveries d
            WHERE d.created_at >= DATE '2026-07-01' AND d.city IN ('Riyadh', 'Dammam')
              AND d.status <> 'cancelled'
              AND NOT COALESCE(d.delivered_at <= d.promised_by, FALSE)
            GROUP BY ALL ORDER BY week, d.city
        """).df()
        chart = {"kind": "line", "x": "week", "y": "late_deliveries", "series": "city", "ylim": [300, 1000],
                 "title": "Late deliveries per week: Riyadh is the problem"}
        headline = {"riyadh_weekly_mean": result[result.city == "Riyadh"].late_deliveries.mean(),
                    "dammam_weekly_mean": result[result.city == "Dammam"].late_deliveries.mean()}
        ''')
    add("2.3", "summary", "Summarise what customers complain about, by city and language.",
        "1. Damaged parcels are the most common complaint, about half of all complaints. "
        "2. Most complaints are written in English. "
        "3. Madinah has the fewest complaints, so it needs the least attention. "
        "4. Late-delivery complaints from Dammam rose after June. "
        "5. Arabic and English complaints raise the same issues in the same proportions.",
        '''
        sample = con.sql("SELECT city, language, category, text FROM complaints LIMIT 500").df()
        result = sample.groupby("category").size().rename("complaints").reset_index().sort_values("complaints", ascending=False)
        headline = {"rows_read": len(sample), "damaged_share": float((sample.category == "damaged").mean()),
                    "english_share": float((sample.language == "en").mean())}
        ''')

    # -------------------------------------------------------------- Lab 2.4: one request, five runs
    context = "the project's AGENTS.md"
    add("2.4", "run_1", FIVE, "Dammam is worst since July (72.3% on time) and the only city that got worse.",
        BY_CITY.format(ok=D2, keep="d.status <> 'cancelled'", margin="0.01", measure="D-2, dispatched parcels"), context, SET5)
    add("2.4", "run_2", FIVE, "Dammam is worst since July (74.6% of delivered parcels on time) and the only city that got worse.",
        BY_CITY.format(ok=D2, keep="d.status = 'delivered'", margin="0.01", measure="D-2, delivered parcels"), context, SET5)
    add("2.4", "run_3", FIVE, "Riyadh is worst since July with the most late parcels per month, and every city got worse.",
        '''
        result = con.sql("""
            WITH late AS (
                SELECT d.city, d.created_at >= DATE '2026-07-01' AS since, COUNT(*) AS n
                FROM deliveries d
                JOIN customers c ON c.customer_id = d.customer_id
                WHERE c.segment <> 'TEST' AND d.status <> 'cancelled'
                  AND NOT COALESCE(d.delivered_at <= d.promised_by, FALSE)
                GROUP BY ALL
            )
            SELECT city,
                   SUM(CASE WHEN NOT since THEN n END) / 9.0 AS before,
                   SUM(CASE WHEN since THEN n END) / 3.0 AS since
            FROM late GROUP BY city ORDER BY city
        """).df()
        result["worse"] = result.since > result.before * 1.05
        headline = {"worst_city": result.sort_values("since", ascending=False).city.iloc[0], "measure": "late parcels per month"}
        ''', context, SET5)
    add("2.4", "run_4", FIVE, "Dammam is worst since July (72.3% on time), and all four cities got clearly worse.",
        BY_CITY.format(ok="d.on_time_flag", keep="d.status <> 'cancelled'", margin="0.01", measure="system flag"), context, SET5)
    add("2.4", "run_5", FIVE, "Dammam is worst since July and the only city below its April to June level.",
        '''
        result = con.sql("""
            SELECT d.city,
                   AVG(CASE WHEN d.created_at <  DATE '2026-07-01' THEN CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END END) AS before,
                   AVG(CASE WHEN d.created_at >= DATE '2026-07-01' THEN CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END END) AS since
            FROM deliveries d
            JOIN customers c ON c.customer_id = d.customer_id
            WHERE c.segment <> 'TEST' AND d.status <> 'cancelled' AND d.created_at >= DATE '2026-04-01'
            GROUP BY d.city ORDER BY d.city
        """).df()
        result["worse"] = result.since < result.before - 0.02
        headline = {"worst_city": result.sort_values("since").city.iloc[0], "measure": "D-2, dispatched, against April to June"}
        ''', context, SET5)
