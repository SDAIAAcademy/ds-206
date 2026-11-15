"""Recorded replies of Day 3 (scripted for the course; see make_recorded.py). They are the steps of the
supplied package data/packages/dammam_q3, which _tools/make_package.py builds from them."""

SET = {"temperature": 0.2, "top_p": 1.0}
CONTEXT = "the project's AGENTS.md"


def register(add) -> None:
    add("3.3", "dammam_quarters", "Follow the brief: on-time rate for Dammam by quarter, D-2, dispatched parcels, no test shipments.",
        "Dammam by quarter under D-2 on dispatched parcels, test shipments removed, quarter of created_at.",
        '''
        result = con.sql("""
            SELECT year(d.created_at) || 'Q' || quarter(d.created_at) AS quarter,
                   COUNT(*) AS deliveries,
                   AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END) AS on_time_rate
            FROM deliveries d
            JOIN customers c ON c.customer_id = d.customer_id
            WHERE d.city = 'Dammam' AND c.segment <> 'TEST' AND d.status <> 'cancelled'
            GROUP BY 1 ORDER BY 1
        """).df()
        rates = result.set_index("quarter").on_time_rate
        headline = {"q2_2026": rates["2026Q2"], "q3_2026": rates["2026Q3"]}
        ''', CONTEXT, SET)
    add("3.3", "long_short", "Follow the brief: Dammam, July to September 2026, on-time rate on routes above 60 planned stops against the rest.",
        "Long against short routes, each parcel counted once, classified by the plan in force.",
        '''
        result = con.sql("""
            WITH plan AS (SELECT * FROM route_plans
                          QUALIFY version = MAX(version) OVER (PARTITION BY hub_id, plan_date, route_id))
            SELECT p.planned_stops > 60 AS long_route, COUNT(*) AS parcels,
                   AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END) AS on_time_rate
            FROM deliveries d
            JOIN customers c ON c.customer_id = d.customer_id
            JOIN plan p ON p.hub_id = d.hub_id AND p.plan_date = d.route_date AND p.route_id = d.route_id
            WHERE d.city = 'Dammam' AND c.segment <> 'TEST' AND d.status <> 'cancelled'
              AND d.created_at >= DATE '2026-07-01' AND d.created_at < DATE '2026-10-01'
            GROUP BY 1 ORDER BY 1
        """).df()
        headline = {"short": result.on_time_rate[0], "long": result.on_time_rate[1], "parcels": int(result.parcels.sum())}
        ''', CONTEXT, SET)
    add("3.3", "weekly_chart", "Chart the weekly late rate for Riyadh and Dammam since July, complete weeks, axis from zero.",
        "Weekly late rate for the two cities, complete weeks only.",
        '''
        result = con.sql("""
            SELECT CAST(date_trunc('week', d.created_at) AS DATE) AS week, d.city,
                   AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 0.0 ELSE 1.0 END) AS late_rate
            FROM deliveries d
            JOIN customers c ON c.customer_id = d.customer_id
            WHERE d.created_at >= DATE '2026-07-06' AND d.created_at < DATE '2026-09-28'
              AND d.city IN ('Riyadh', 'Dammam') AND c.segment <> 'TEST' AND d.status <> 'cancelled'
            GROUP BY ALL ORDER BY week, d.city
        """).df()
        headline = {"weeks": int(result.week.nunique()), "dammam_mean_late_rate": float(result[result.city == "Dammam"].late_rate.mean())}
        ''', CONTEXT, SET)
