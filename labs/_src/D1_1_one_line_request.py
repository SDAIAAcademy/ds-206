# %% [markdown]
# # Lab 1.1 · One line in, six assumptions out
#
# Day 1 · Session 1 (What assistants get wrong in analysis) · 25 min.
#
# Tahani Al-Qasim, operations director of Hudhud Parcel, wants one number. You give Rafiq, the notebook
# assistant, a one-line request, run what it writes, and list every choice it made for you. Then you test
# three of those choices with one query each and see how far the number moves.
#
# **AI policy for this lab:** AI-full. The assistant is the subject.
#
# **Tasks**
# - [ ] 1 · Send the one-line request and run the reply (5 min)
# - [ ] 2 · List every assumption in the reply's code (8 min)
# - [ ] 3 · Test three assumptions with one query each (8 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Send the same line to your own assistant and compare its assumptions

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
# ## 1 · Send the one-line request and run the reply
#
# `U.ask` sends the request to a free hosted model when `OPENROUTER_API_KEY` is set. The model is shown
# table and column names only, never rows. With no key the lab continues with the recorded reply.
# The checked steps below always use the **recorded** reply, so the whole room checks the same code.

# %%
REQUEST = "What is our on-time delivery rate?"

live = U.ask(REQUEST, c=con)                 # None without a key
reply = U.recorded("1.1", "one_line")        # the recorded reply the lab checks
U.show(reply)
out = U.run_reply(reply, con)
print("\nheadline:", out.headline, "| rows counted:", int(out.result.loc[0, "deliveries"]))
if live:
    print("\nYour live reply, for comparison:")
    U.show(live)
    print("headline:", U.run_reply(live, con).headline)

# %% [markdown]
# **Look at** the reply's sentence and its code side by side. The sentence says "on-time delivery rate".
# The code decides what that means. Open `data/docs/definitions.md` before the next task.

# %%
print(U.load("docs/definitions.md"))

# %% [markdown]
# ## 2 · List every assumption in the reply's code
#
# ✏️ **Exercise** · Return a list of sentences, one per choice the assistant made that you did not ask for.
# Read the code line by line: the column it averaged, each join, each filter, what is in the denominator,
# which period and which groups are pooled. Aim for six.

# %%
def my_assumptions():
    # BEGIN SOLUTION
    return [
        "It took on_time_flag as the meaning of on time: the flag mixes definition D-1 before April with D-2 after",
        "It joined deliveries to scans: a parcel whose scan was uploaded twice is counted twice",
        "It kept only parcels with a delivered scan: failed and returned parcels left the denominator",
        "It kept test shipments: the customers table and its TEST segment were never read",
        "It pooled the whole year into one number: no month, no before and after April",
        "It pooled four cities and both services, standard and express",
    ]
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
THEMES = {"the definition behind the flag": r"flag|definition|D-1|D-2", "the join to scans": r"scan|join|twice|duplicate",
          "failed parcels and the denominator": r"failed|returned|denominator|delivered scan", "test shipments": r"test",
          "the pooled year": r"year|month|april|period", "pooled cities and services": r"cit|service|express"}
try:
    assumptions = my_assumptions()
except NotImplementedError:
    assumptions = U.load("reference/lab_1_1_assumptions.json")
import re
found = [t for t, pat in THEMES.items() if any(re.search(pat, a, re.I) for a in assumptions)]
for t in THEMES:
    print("✓" if t in found else "·", t)
U.check(len(assumptions) >= 5 and len(found) >= 5, f"{len(assumptions)} assumptions listed, {len(found)} of 6 themes covered")

# %% [markdown]
# ## 3 · Test three assumptions with one query each
#
# An assumption is tested by changing it and watching the number. `on_time_rate` below computes the rate
# for a chosen definition and denominator; two of its pieces are missing.
#
# ✏️ **Exercise** · Add definition D-2 and the dispatched denominator, both from `definitions.md`:
# `OK["D-2"]` is a SQL expression that is 1 when the parcel was delivered at or before `promised_by` and 0
# otherwise (an undelivered parcel is 0); `KEEP["dispatched"]` is a SQL condition that drops cancelled orders.

# %%
OK = {"flag": "d.on_time_flag",
      "D-1": "CASE WHEN CAST(d.delivered_at AS DATE) <= d.promised_date THEN 1 ELSE 0 END"}
KEEP = {"all": "TRUE", "delivered": "d.status = 'delivered'"}


def add_d2():
    # BEGIN SOLUTION
    OK["D-2"] = "CASE WHEN d.delivered_at <= d.promised_by THEN 1 ELSE 0 END"
    KEEP["dispatched"] = "d.status <> 'cancelled'"
    # END SOLUTION


def on_time_rate(con, definition="D-2", drop_tests=True, denominator="dispatched"):
    tests = "c.segment <> 'TEST'" if drop_tests else "TRUE"
    sql = f"""SELECT AVG({OK[definition]})
              FROM deliveries d JOIN customers c ON c.customer_id = d.customer_id
              WHERE {KEEP[denominator]} AND {tests}"""
    return round(U.one(con, sql), 4)

# %%
# Check, with a safety net
try:
    add_d2()
except NotImplementedError:
    snippets = U.load("reference/snippets.json")
    OK["D-2"], KEEP["dispatched"] = snippets["d2_ok"], snippets["dispatched"]

table = pd.DataFrame([
    ("the reply: flag, joined to delivered scans, tests kept", out.headline["on_time_rate"]),
    ("flag, one row per parcel, tests kept", on_time_rate(con, "flag", drop_tests=False, denominator="all")),
    ("flag, one row per parcel, no tests", on_time_rate(con, "flag", denominator="all")),
    ("D-1 for the whole year, delivered parcels only", on_time_rate(con, "D-1", denominator="delivered")),
    ("D-2 for the whole year, delivered parcels only", on_time_rate(con, "D-2", denominator="delivered")),
    ("D-2 for the whole year, dispatched parcels (definitions.md)", on_time_rate(con)),
], columns=["what was assumed", "on_time_rate"])
print(table.to_string(index=False))
canonical = on_time_rate(con)
U.check(abs(canonical - U.reference("on_time")) < 1e-4, f"your D-2 rate {canonical:.4f} equals the planted answer")
spread = table.on_time_rate.max() - table.on_time_rate.min()
print(f"\nOne question, {len(table)} defensible-looking numbers, {spread * 100:.1f} points apart.")

# %% [markdown]
# **Look at** the table. Nothing in it is a bug in the usual sense: every row runs, and every row is
# "the on-time rate" under some reading. Which row would Tahani have quoted to the board?

# %% [markdown]
# ## 4 · Write the verification note
#
# Every lab of this course ends the same way: three sentences that someone else can check.
#
# ✏️ **Exercise** · Fill the three parts. Put the numbers in.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"One SQL query and the sentence 'on-time rate is 85.3%' (it computed {out.headline['on_time_rate']:.4f}) for a one-line request.",
        checked="Read the code line by line, listed six assumptions, then changed three of them (definition, denominator, tests) one query at a time against definitions.md.",
        wrong=f"The flag mixes D-1 and D-2, failed parcels and duplicated scans distort the count, tests were kept: under D-2 on dispatched parcels the rate is {canonical:.4f}.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["1.1"]
note = U.note("1.1", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Send the same one line to the assistant you use at work (on synthetic data only) or rerun `U.ask` a second
# time. List its assumptions the same way. Which differ from the recorded reply's, and which are the same?
#
# ## Check yourself
#
# 1. The reply ran without an error and returned a number between 0 and 1. What does that tell you?
# 2. Which assumption moved the number most?
# 3. Why did the join to scans change a rate, when a rate is a ratio?
#
# <details><summary>Answers</summary>
#
# 1. That the code is valid SQL. Nothing about whether it answers the question that was meant.
# 2. The definition: the flag mixes a lenient rule and a strict one, and D-1 against D-2 is about ten points.
# 3. The duplicated rows are not spread evenly: they sit in Jeddah in March and April, and failed parcels
#    have no delivered scan at all, so the join changed which parcels were counted, not only how many.
#
# </details>
#
# ## Carry forward
#
# Your note is in `artifacts/notes/lab_1_1.md`. Lab 1.3 turns the assumptions you listed into a brief that
# states them before the assistant runs. It starts from its own supplied files.
