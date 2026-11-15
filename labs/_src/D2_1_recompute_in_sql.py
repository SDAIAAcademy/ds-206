# %% [markdown]
# # Lab 2.1 · Recompute and reconcile
#
# Day 2 · Session 1 (Recompute it another way) · 25 min.
#
# Rafiq analysed Dammam by quarter in pandas and reports no clear deterioration. You recompute the same
# rate in SQL, from the definitions and without an assistant, find a different number, and then explain
# the whole gap: one cause per row, until the two numbers meet.
#
# **AI policy for this lab:** AI-off for task 2, the first recomputation. It is the evidence that the
# number is yours.
#
# **Tasks**
# - [ ] 1 · Run the assisted analysis and read its number (4 min)
# - [ ] 2 · Recompute the rate yourself in SQL, without an assistant (8 min)
# - [ ] 3 · Reconcile the gap, one cause per row (9 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Recompute a third time in pandas from the parquet file

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
# ## 1 · Run the assisted analysis and read its number
#
# The request was: "On-time rate for Dammam by quarter. Did the third quarter of 2026 get worse?"

# %%
reply = U.recorded("2.1", "dammam_quarters")
U.show(reply)
out = U.run_reply(reply, con)
print("\n" + out.result.round(4).to_string(index=False))
theirs = out.headline["q3_2026"]
print(f"\nRafiq's third quarter of 2026: {theirs:.4f}")

# %% [markdown]
# ## 2 · Recompute the rate yourself in SQL
#
# Close the reply. Open `data/docs/definitions.md` (the notebook printed it in Lab 1.1; `print(U.load("docs/definitions.md"))`
# shows it again). Work from the `deliveries` table, not from Rafiq's code: a recomputation that copies the
# first path's choices verifies nothing.
#
# ✏️ **Exercise** · Return a table with `quarter` (as `2025Q4` ... `2026Q3`), `deliveries` and `on_time_rate`
# for Dammam: definition D-2, dispatched parcels, no test shipments, quarter of `created_at`.

# %%
def my_dammam() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, """
        SELECT year(d.created_at) || 'Q' || quarter(d.created_at) AS quarter,
               COUNT(*) AS deliveries,
               AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 1.0 ELSE 0.0 END) AS on_time_rate
        FROM deliveries d
        JOIN customers c ON c.customer_id = d.customer_id
        WHERE d.city = 'Dammam' AND c.segment <> 'TEST' AND d.status <> 'cancelled'
        GROUP BY 1 ORDER BY 1
    """)
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    mine_table = my_dammam()
except NotImplementedError:
    mine_table = pd.DataFrame(U.load("reference/lab_2_1_mine.json"))
U.keep("lab_2_1_mine.json", mine_table.to_dict("records"))
print(mine_table.round(4).to_string(index=False))
planted = U.reference("dammam_by_quarter")
for q, rate in zip(mine_table.quarter, mine_table.on_time_rate):
    U.check(abs(rate - planted[q]) < 1e-4, f"{q}: your {rate:.4f} equals the planted answer")
mine = float(mine_table.set_index("quarter").on_time_rate["2026Q3"])
gap = theirs - mine
print(f"\nRafiq {theirs:.4f}, you {mine:.4f}: a gap of {gap * 100:.1f} points in the third quarter.")
print(f"Change from the second quarter: Rafiq {(out.headline['q3_2026'] - out.headline['q2_2026']) * 100:+.1f} points, "
      f"you {(mine - planted['2026Q2']) * 100:+.1f} points.")

# %% [markdown]
# **Look at** the two stories. Rafiq: steady, a dip of under three points. You: a fall of more than seven.
# Two numbers that differ are not yet a finding. Until the gap is explained, you do not know which is wrong.

# %% [markdown]
# ## 3 · Reconcile the gap, one cause per row
#
# `variant()` reruns Rafiq's method for the third quarter with some of its choices replaced. With no
# argument it reproduces Rafiq's number; with all four it follows `definitions.md`.
#
# | Argument | Rafiq's choice | Replaced by |
# |---|---|---|
# | `local_time` | compares `scan_time_utc` with the local promise | scan time plus three hours |
# | `by_created` | quarter of the scan | quarter of `created_at` |
# | `dispatched` | only parcels that have a delivered scan | every dispatched parcel; undelivered ones are late |
# | `drop_tests` | test shipments kept | test shipments removed |
#
# ✏️ **Exercise** · Return a table with one row per step, in the order of the table above, each row adding
# one replacement to the ones before: columns `step`, `rate` and `delta` (the change from the row above,
# 0 for the first row). The first row is Rafiq's number, the last must equal yours.

# %%
def variant(local_time=False, by_created=False, dispatched=False, drop_tests=False) -> float:
    t = "s.scan_time_utc + INTERVAL 3 HOUR" if local_time else "s.scan_time_utc"
    quarter_of = "d.created_at" if by_created else "s.scan_time_utc"
    join = "LEFT JOIN" if dispatched else "JOIN"
    keep = ("d.status <> 'cancelled'" if dispatched else "TRUE") + (" AND c.segment <> 'TEST'" if drop_tests else "")
    return float(U.one(con, f"""
        SELECT AVG(CASE WHEN {t} <= d.promised_by THEN 1.0 ELSE 0.0 END)
        FROM deliveries d
        JOIN customers c ON c.customer_id = d.customer_id
        {join} scans s ON s.delivery_id = d.delivery_id AND s.outcome = 'delivered'
        WHERE d.city = 'Dammam' AND {keep}
          AND year({quarter_of}) || 'Q' || quarter({quarter_of}) = '2026Q3'"""))


def reconcile() -> pd.DataFrame:
    # BEGIN SOLUTION
    steps = [("Rafiq's method", {}),
             ("+ compare in local time", {"local_time": True}),
             ("+ quarter of created_at", {"local_time": True, "by_created": True}),
             ("+ every dispatched parcel", {"local_time": True, "by_created": True, "dispatched": True}),
             ("+ no test shipments", {"local_time": True, "by_created": True, "dispatched": True, "drop_tests": True})]
    table = pd.DataFrame([{"step": name, "rate": variant(**kw)} for name, kw in steps])
    table["delta"] = table.rate.diff().fillna(0.0)
    return table
    # END SOLUTION

# %%
# Check, with a safety net
try:
    bridge = reconcile()
except NotImplementedError:
    bridge = pd.DataFrame(U.load("reference/lab_2_1_bridge.json"))
U.keep("lab_2_1_bridge.json", bridge.to_dict("records"))
print(bridge.assign(rate=bridge.rate.round(4), points=(bridge.delta * 100).round(2)).drop(columns="delta").to_string(index=False))
U.check(abs(bridge.rate.iloc[0] - theirs) < 1e-4, "the first row reproduces Rafiq's number")
U.check(abs(bridge.rate.iloc[-1] - mine) < 1e-4, "the last row equals your number")
U.check(abs(bridge.delta.sum() - (mine - theirs)) < 1e-4, f"the rows explain the whole gap of {gap * 100:.1f} points, nothing is left over")
biggest = bridge.loc[bridge.delta.abs().idxmax(), "step"]
print(f"\nThe largest cause: {biggest} ({bridge.delta.abs().max() * 100:.1f} points).")

# %% [markdown]
# **Look at** the largest row. Parcels delivered in the three hours after the cut-off looked on time,
# because a UTC scan was compared with a local promise. Dammam's problem in the third quarter is evening
# deliveries. The one error in the method hid the one thing the director needed to see.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts, with the numbers.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"A pandas analysis of Dammam by quarter: {theirs:.4f} on time in 2026Q3 and the sentence 'a dip of under three points'.",
        checked=f"Recomputed in SQL from definitions.md without an assistant ({mine:.4f}), then reconciled the {gap * 100:.1f}-point gap in four steps until both numbers met.",
        wrong=f"UTC scan times against local promises ({bridge.delta.iloc[1] * 100:+.1f} points), undelivered parcels missing from the denominator ({bridge.delta.iloc[3] * 100:+.1f}); quarter and tests moved little. The real fall from Q2 is {(mine - planted['2026Q2']) * 100:.1f} points.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["2.1"]
note = U.note("2.1", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Recompute the third-quarter rate a third time with pandas only: `pd.read_parquet(U.STORE / "deliveries.parquet")`
# and `customers.parquet`, no SQL. Three paths, one number.
#
# ## Check yourself
#
# 1. Your SQL gave a different number from Rafiq's pandas. Why is that not yet a result?
# 2. Why does the reconciliation change one thing per row?
# 3. Rafiq's code and yours used different engines. Was that what made your recomputation independent?
#
# <details><summary>Answers</summary>
#
# 1. A gap says one of the two is wrong, or both. Only an explained gap says which, and why.
# 2. So that every point of the gap has one named cause, and so that nothing is left over that hides a
#    second error.
# 3. Only partly. What made it independent is that it started from the definitions and the parcel table,
#    not from the first path's joins and choices. The same wrong join in another engine verifies nothing.
#
# </details>
#
# ## Carry forward
#
# The Dammam fall is now a checked number. Lab 2.2 tests the first explanation for it: long routes.
