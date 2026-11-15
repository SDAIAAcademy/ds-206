# %% [markdown]
# # Lab 1.3 · A brief with acceptance checks
#
# Day 1 · Session 3 (The delegation brief) · 25 min.
#
# You complete a delegation brief for three steps of the plan (clean, monthly rate, chart), write three
# of its acceptance checks as code, run the brief and apply the checks to what comes back. One check
# fails; you send one follow-up and apply the checks again.
#
# **AI policy for this lab:** AI-full for running the brief. You write the checks yourself.
#
# **Tasks**
# - [ ] 1 · Complete the brief until it has no gaps (8 min)
# - [ ] 2 · Write three acceptance checks as functions (8 min)
# - [ ] 3 · Run the brief, apply the checks, follow up once (5 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Add a check that would have caught the flag's two definitions

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
# ## 1 · Complete the brief
#
# A brief has five parts: the **question**, the **data**, the **definitions**, the **constraints** and the
# **acceptance checks**. The first two are written. `U.brief_gaps` lists what a reviewer would send back.
#
# ✏️ **Exercise** · Fill `definitions`, `constraints` and at least three `acceptance_checks`. A check is a
# sentence a reviewer can apply without asking you: it names a number, a count or a condition.

# %%
brief = {
    "question": "For Tahani Al-Qasim: the monthly on-time rate of Hudhud Parcel from October 2025 to September 2026, as a table and one chart.",
    "data": "deliveries (one row per parcel) and customers (for the segment). Month is the month of created_at. Do not join scans.",
    "steps": ["1 · working table without test shipments and cancelled orders", "2 · monthly on-time rate", "3 · line chart of the monthly rate"],
}


def complete(brief: dict) -> dict:
    # BEGIN SOLUTION
    brief["definitions"] = ("On time is D-2 for every month: delivered_at at or before promised_by; a dispatched parcel "
                            "that was never delivered is late. Do not use on_time_flag.")
    brief["constraints"] = ("SQL in DuckDB, one query per step. No test shipments (segment TEST), no cancelled orders. "
                            "Stop after each step and show its row count before the next.")
    brief["acceptance_checks"] = [
        "The deliveries of the 12 months sum to the number of dispatched, non-test parcels, which I count myself",
        "Exactly 12 rows, one per month from 2025-10 to 2026-09, none missing and none extra",
        "Every rate is between 0 and 1, and no month differs from the month before by more than 5 points",
    ]
    return brief
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    brief = complete(brief)
except NotImplementedError:
    brief.update(U.load("reference/brief.json"))
gaps = U.brief_gaps(brief)
print(U.render_brief(brief), "\n\ngaps:", gaps)
U.check(gaps == [], "the brief has all five parts and three checks a reviewer can apply")
U.keep("brief.json", {k: brief[k] for k in ("definitions", "constraints", "acceptance_checks")})

# %% [markdown]
# ## 2 · Write three acceptance checks as functions
#
# The reply's code sets `result`: one row per month with `month`, `deliveries` and `on_time_rate`.
# Each check takes that table and returns `(passed, what_it_saw)`.
#
# ✏️ **Exercise** · Write the three functions. For the first, count the dispatched, non-test parcels with
# your own query: the expected number must not come from the assistant.

# %%
def check_total(result) -> tuple[bool, str]:
    # BEGIN SOLUTION
    expected = U.one(con, """SELECT COUNT(*) FROM deliveries d JOIN customers c ON c.customer_id = d.customer_id
                             WHERE c.segment <> 'TEST' AND d.status <> 'cancelled'""")
    got = int(result["deliveries"].sum())
    return got == expected, f"table sums to {got:,}, dispatched non-test parcels are {expected:,}"
    # END SOLUTION


def check_months(result) -> tuple[bool, str]:
    # BEGIN SOLUTION
    want = [str(p) for p in pd.period_range("2025-10", "2026-09", freq="M")]
    got = list(result["month"])
    return got == want, f"{len(got)} rows, from {got[0]} to {got[-1]}"
    # END SOLUTION


def check_rates(result) -> tuple[bool, str]:
    # BEGIN SOLUTION
    r = result["on_time_rate"]
    jump = float(r.diff().abs().max())
    return bool(r.between(0, 1).all() and jump <= 0.05), f"rates {r.min():.3f} to {r.max():.3f}, largest month-to-month change {jump * 100:.1f} points"
    # END SOLUTION


CHECKS = [check_total, check_months, check_rates]

# %% [markdown]
# ## 3 · Run the brief, apply the checks, follow up once
#
# The brief goes to the assistant as one request. The recorded first reply is `brief_v1`.

# %%
def apply_checks(result) -> pd.DataFrame:
    rows = []
    for fn in CHECKS:
        try:
            ok, saw = fn(result)
        except NotImplementedError:      # safety net: the reference implementation of the same check
            ok, saw = U.reference_check(fn.__name__, result, con)
        rows.append({"check": fn.__name__, "passed": ok, "saw": saw})
    return pd.DataFrame(rows)


request = U.render_brief(brief) + "\n\nDo step 2: the monthly on-time rate."
live = U.ask(request, c=con, tables=["deliveries", "customers"])
v1 = U.recorded("1.3", "brief_v1")
U.show(v1)
out1 = U.run_reply(v1, con)
first = apply_checks(out1.result)
print("\n" + first.to_string(index=False), "\nheadline:", out1.headline)
U.check(list(first.passed) == [False, True, True], "the first reply fails the total and passes the other two checks")

# %% [markdown]
# The failed check tells you what to say next: not "this looks wrong", but the check, the number it saw
# and the rule it broke. That is the follow-up that was recorded as `brief_v2`.

# %%
v2 = U.recorded("1.3", "brief_v2")
print("follow-up sent:", v2.request, "\n")
U.show(v2)
out2 = U.run_reply(v2, con)
second = apply_checks(out2.result)
print("\n" + second.to_string(index=False), "\nheadline:", out2.headline)
U.check(bool(second.passed.all()), "the second reply passes all three checks")
U.check(abs(out2.headline["on_time_rate"] - U.reference("on_time")) < 1e-4, "and its yearly rate equals the planted answer")
print(out2.result.round(4).to_string(index=False))
if live:
    print("\nYour live reply against the same checks:")
    lo = U.run_reply(live, con)
    try:
        print(lo.error or apply_checks(lo.result).to_string(index=False))
    except Exception as e:           # a live reply in another shape is a finding, not a crash
        print(f"The checks could not be applied ({type(e).__name__}: {e}): the reply did not return the table the brief asks for.")

# %% [markdown]
# **Look at** the two headline numbers. Both replies were fluent, and both said "under D-2, without test
# shipments". Only the check you wrote before running told them apart.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts, with the numbers.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"A monthly on-time table under D-2; first reply {out1.headline['on_time_rate']:.4f} for the year, second reply {out2.headline['on_time_rate']:.4f}.",
        checked="Three acceptance checks written before the run: the total against my own count of dispatched parcels, twelve months, rates in range without a 5-point jump.",
        wrong=f"The first reply kept cancelled orders: its table summed to {int(out1.result.deliveries.sum()):,} against {int(out2.result.deliveries.sum()):,} dispatched parcels; one follow-up fixed it.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["1.3"]
note = U.note("1.3", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Run `check_rates` on a monthly table built from `on_time_flag` (Lab 1.1's first assumption). Does your
# 5-point rule catch the April change of definition? Write the check that would say why.
#
# ## Check yourself
#
# 1. "The numbers should look reasonable." Why is that not an acceptance check?
# 2. Why must the expected total come from your own query?
# 3. The brief says "stop after each step". What does that buy you?
#
# <details><summary>Answers</summary>
#
# 1. A reviewer cannot apply it without asking the author what reasonable means. A check names a number,
#    a count or a condition.
# 2. A check that reuses the assistant's number compares the answer with itself and always passes.
# 3. An error is found one step after it is made, with one step of code to read, not at the end with all of it.
#
# </details>
#
# ## Carry forward
#
# The three checks return in Lab 1.4 as `U.reference_check`, so that lab does not need this one.
