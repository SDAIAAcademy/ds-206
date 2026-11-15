# %% [markdown]
# # Lab 2.2 · Four seeded errors
#
# Day 2 · Session 2 (Joins, filters and denominators) · 25 min.
#
# Rafiq compared long routes with short ones in Dammam for July to September 2026. Its query has four
# seeded errors: two in joins, two in filters. You find them with three checks: row counts around each
# join, an anti-join against the scope, and the denominator said aloud.
#
# **AI policy for this lab:** AI-off for the checks. You may ask the assistant to explain SQL syntax.
#
# **Tasks**
# - [ ] 1 · Run the assisted analysis and read its claim (4 min)
# - [ ] 2 · Count rows before and after each join (7 min)
# - [ ] 3 · Find the rows each filter dropped (6 min)
# - [ ] 4 · State the denominator and recompute (4 min)
# - [ ] 5 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Repair the query and confirm the corrected comparison

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-206.git"
    if not Path("/content/ds-206").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-206"], check=True)
    os.chdir("/content/ds-206/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import pandas as pd
import hudhud as U

pd.set_option("display.width", 160)
con = U.con()  # the first call builds the synthetic tables, once (about 20 seconds)

# %% [markdown]
# ## 1 · Run the assisted analysis and read its claim

# %%
reply = U.recorded("2.2", "long_routes")
U.show(reply)
out = U.run_reply(reply, con)
print("\n" + out.result.round(4).to_string(index=False))
print("parcels in the comparison:", int(out.headline["parcels"]))

# %% [markdown]
# ## 2 · Count rows before and after each join
#
# The scope sentence is: *Dammam parcels created from 1 July to 30 September 2026, dispatched, no test
# shipments.* One row must be one parcel at every stage. The pieces of Rafiq's query are below.
#
# ✏️ **Exercise** · `profile(sql)` takes a query that returns `delivery_id` and returns
# `(rows, distinct_parcels)`.

# %%
FROM = "FROM deliveries d JOIN customers c ON c.customer_id = d.customer_id"
PLANS = "JOIN route_plans p ON p.hub_id = d.hub_id AND p.plan_date = d.route_date AND p.route_id = d.route_id"
SHIFTS = "LEFT JOIN driver_shifts s ON s.driver_id = d.driver_id AND s.shift_date = d.route_date"
WHERE = ("WHERE d.city = 'Dammam' AND c.segment <> 'TEST' "
         "AND d.created_at BETWEEN '2026-07-01' AND '2026-09-30' AND d.status = 'delivered'")
STAGES = {
    "deliveries, Rafiq's filters": f"SELECT d.delivery_id {FROM} {WHERE}",
    "+ join route_plans": f"SELECT d.delivery_id {FROM} {PLANS} {WHERE}",
    "+ left join driver_shifts": f"SELECT d.delivery_id {FROM} {PLANS} {SHIFTS} {WHERE}",
    "+ AND s.hours >= 8": f"SELECT d.delivery_id {FROM} {PLANS} {SHIFTS} {WHERE} AND s.hours >= 8",
}


def profile(sql: str) -> tuple[int, int]:
    # BEGIN SOLUTION
    return U.q(con, f"SELECT COUNT(*) AS n, COUNT(DISTINCT delivery_id) AS u FROM ({sql})").iloc[0].astype(int).tolist()
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    stages = pd.DataFrame([(name, *profile(sql)) for name, sql in STAGES.items()], columns=["stage", "rows", "parcels"])
except NotImplementedError:
    stages = pd.DataFrame(U.load("reference/lab_2_2_stages.json"))
U.keep("lab_2_2_stages.json", stages.to_dict("records"))
stages["rows_per_parcel"] = (stages["rows"] / stages["parcels"]).round(4)
print(stages.to_string(index=False))
U.check(stages.rows[0] == stages.parcels[0], "before any join, one row is one parcel")
U.check(stages.rows[1] > stages.parcels[1], f"the join to route_plans fans out: {stages.rows[1] - stages.parcels[1]:,} extra rows (error 1: plan versions)")
U.check(stages.parcels[3] < stages.parcels[2], f"the filter on the shift table removes {stages.parcels[2] - stages.parcels[3]:,} parcels (error 2: a left join made inner)")

# %% [markdown]
# **Look at** the last two rows. The left join to `driver_shifts` added rows (split shifts have two rows).
# Then `s.hours >= 8` in the `WHERE` clause removed every parcel whose driver had no single shift of eight
# hours: the left join became an inner join, and nobody asked for "full shifts only".

# %% [markdown]
# ## 3 · Find the rows each filter dropped
#
# An anti-join answers "which parcels of the scope are not in the result?". The scope is written from the
# sentence, not from Rafiq's filters.
#
# ✏️ **Exercise** · Return a table `reason`, `parcels`: the parcels of `SCOPE` that are missing from
# Rafiq's joined rows (`J`), with the reason given by the `REASON` expression.

# %%
SCOPE = f"""SELECT d.* {FROM}
            WHERE d.city = 'Dammam' AND c.segment <> 'TEST' AND d.status <> 'cancelled'
              AND d.created_at >= DATE '2026-07-01' AND d.created_at < DATE '2026-10-01'"""
J = STAGES["+ AND s.hours >= 8"]
REASON = """CASE WHEN status <> 'delivered' THEN 'never delivered: failed or returned'
                 WHEN CAST(created_at AS DATE) = DATE '2026-09-30' THEN 'created on the last day'
                 ELSE 'driver on a split shift' END"""


def dropped() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, f"""
        WITH scope AS ({SCOPE}), j AS (SELECT DISTINCT delivery_id FROM ({J}))
        SELECT {REASON} AS reason, COUNT(*) AS parcels
        FROM scope LEFT JOIN j ON j.delivery_id = scope.delivery_id
        WHERE j.delivery_id IS NULL
        GROUP BY 1 ORDER BY 2 DESC""")
    # END SOLUTION

# %%
# Check, with a safety net
try:
    lost = dropped()
except NotImplementedError:
    lost = pd.DataFrame(U.load("reference/lab_2_2_dropped.json"))
U.keep("lab_2_2_dropped.json", lost.to_dict("records"))
print(lost.to_string(index=False))
in_scope = int(U.one(con, f"SELECT COUNT(*) FROM ({SCOPE})"))
print(f"\nscope: {in_scope:,} parcels; missing from Rafiq's rows: {int(lost.parcels.sum()):,}")
U.check(set(lost.reason) == {"never delivered: failed or returned", "created on the last day", "driver on a split shift"},
        "three kinds of parcel were dropped (errors 2, 3 and 4)")
U.check(in_scope == U.reference("dammam_q3_long_short")["long"][0] + U.reference("dammam_q3_long_short")["short"][0],
        "your scope has the planted number of parcels")

# %% [markdown]
# ## 4 · State the denominator and recompute
#
# The denominator sentence: *dispatched Dammam parcels created in the three months, each counted once,
# classified by the plan in force (the highest version) on its route and day.*
#
# ✏️ **Exercise** · Return `long_route`, `parcels`, `on_time_rate` for that sentence. `QUALIFY` keeps the
# highest version of each plan.

# %%
def corrected() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, f"""
        WITH scope AS ({SCOPE}),
        plan AS (SELECT * FROM route_plans
                 QUALIFY version = MAX(version) OVER (PARTITION BY hub_id, plan_date, route_id))
        SELECT p.planned_stops > 60 AS long_route, COUNT(*) AS parcels,
               AVG(CASE WHEN s.delivered_at <= s.promised_by THEN 1.0 ELSE 0.0 END) AS on_time_rate
        FROM scope s
        JOIN plan p ON p.hub_id = s.hub_id AND p.plan_date = s.route_date AND p.route_id = s.route_id
        GROUP BY 1 ORDER BY 1""")
    # END SOLUTION

# %%
# Check, with a safety net
try:
    fixed = corrected()
except NotImplementedError:
    fixed = pd.DataFrame(U.load("reference/lab_2_2_fixed.json"))
U.keep("lab_2_2_fixed.json", fixed.to_dict("records"))
both = pd.DataFrame({"route": ["short", "long"], "rafiq_parcels": out.result.parcels.astype(int), "rafiq_rate": out.result.on_time_rate.round(4),
                     "parcels": fixed.parcels.astype(int), "on_time_rate": fixed.on_time_rate.round(4)})
print(both.to_string(index=False))
planted = U.reference("dammam_q3_long_short")
U.check(int(fixed.parcels.sum()) == in_scope, "every parcel of the scope is counted once")
U.check(abs(fixed.on_time_rate[1] - planted["long"][1]) < 1e-4 and abs(fixed.on_time_rate[0] - planted["short"][1]) < 1e-4,
        "both corrected rates equal the planted answers")
print(f"\ngap long against short: Rafiq {(out.headline['short'] - out.headline['long']) * 100:.1f} points, corrected {(fixed.on_time_rate[0] - fixed.on_time_rate[1]) * 100:.1f} points")

# %% [markdown]
# **Look at** what survived. The conclusion did: long routes are on time about eleven points less often.
# The two rates did not: each was more than two points too high, and the parcel count was wrong. A report
# quotes the rates. "The direction was right" is not a defence for a number.

# %% [markdown]
# ## 5 · Write the verification note
#
# The course outcome asks for a note that names each error and the check that found it.
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"A SQL comparison of long and short routes in Dammam: {out.headline['long']:.4f} against {out.headline['short']:.4f} on {int(out.headline['parcels']):,} rows that it counted as parcels.",
        checked="Row counts before and after each join, an anti-join of the scope against the joined rows, and the denominator written as a sentence and recomputed.",
        wrong=(f"Four errors. 1 plan versions fan out the join (row count). 2 a filter on driver_shifts made the left join inner and dropped split-shift drivers (row count, anti-join). "
               f"3 BETWEEN dropped the last day (anti-join). 4 delivered-only dropped failed parcels (anti-join, denominator). Corrected: {fixed.on_time_rate[1]:.4f} against {fixed.on_time_rate[0]:.4f} on {in_scope:,} parcels."),
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["2.2"]
note = U.note("2.2", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Repair Rafiq's query in place, changing as little as you can, until it returns the corrected table.
# Which of the four repairs changed the rates most?
#
# ## Check yourself
#
# 1. Which single check finds a fan-out fastest?
# 2. `BETWEEN '2026-07-01' AND '2026-09-30'` on a timestamp: what is lost?
# 3. Rafiq's conclusion was right. Why does the note still list four errors?
#
# <details><summary>Answers</summary>
#
# 1. Rows against distinct keys after the join. If they differ, one parcel has become several rows.
# 2. Everything after midnight at the start of 30 September: the last day.
# 3. The report quotes numbers, and both were wrong. A conclusion that survives errors this time will
#    not survive them the next time the same query is reused.
#
# </details>
#
# ## Carry forward
#
# Long routes go with late parcels in Dammam. Whether the optimiser causes it is step 7 of the plan: kept.
