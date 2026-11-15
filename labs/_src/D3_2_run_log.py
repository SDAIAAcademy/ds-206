# %% [markdown]
# # Lab 3.2 · A run log
#
# Day 3 · Session 2 (Logging assisted work) · 25 min.
#
# A colleague must be able to rerun your assisted step next month without asking you anything. You read
# a log that cannot be rerun, write a log record that can, with a fingerprint of the data it ran on, and
# prove it by rerunning your own step from the log alone.
#
# **AI policy for this lab:** AI-full.
#
# **Tasks**
# - [ ] 1 · Read an incomplete log and list what a rerun lacks (5 min)
# - [ ] 2 · Write the log record and the data fingerprint (9 min)
# - [ ] 3 · Run one analysis through the logger and check the log (7 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Change one row of a table and show that the fingerprint changes

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
# ## 1 · Read an incomplete log and list what a rerun lacks
#
# Three records from a real-looking project log. `U.log_gaps` names the fields a rerun needs and a record
# lacks: the step, the request, the context file's fingerprint, the model, its settings, the code, the
# data's fingerprint, the headline numbers, and how the step was verified.

# %%
import json

old = U.load("logs/incomplete_log.jsonl")
for rec in old:
    print(f"step {rec['seq']} · {rec['step']:13s} lacks: {', '.join(U.log_gaps(rec))}")
print("\nrequest of step 2:", repr(old[1]["request"]), "| code of step 3:", repr(old[2]["code"]))

# %% [markdown]
# **Look at** step 2's request, "same but by city", and step 3's code, "see notebook cell 14". Both made
# sense on the day. Neither can be rerun.

# %% [markdown]
# ## 2 · Write the log record and the data fingerprint
#
# A fingerprint answers "is this the data the step ran on?" without storing the data: the number of rows
# and a hash of a few totals.
#
# ✏️ **Exercise** · `fingerprint(table)` returns `{"rows": ..., "sha": ...}` where `sha` is `U.sha` of a
# list of strings: the row count, and for `deliveries` also the sum of `delivery_id` and the earliest and
# latest `created_at`. For any other table, the row count is enough here.
#
# ✏️ **Exercise** · `log_record(step, reply, outcome, tables, verified_by)` returns a dict with the keys
# `step`, `request`, `context_sha` (`U.sha` of the reply's context), `model`, `settings`, `code`, `data`
# (table name to fingerprint), `headline` and `verified_by`.

# %%
def fingerprint(table: str) -> dict:
    # BEGIN SOLUTION
    if table == "deliveries":
        row = con.sql("SELECT COUNT(*), SUM(delivery_id), CAST(MIN(created_at) AS VARCHAR), CAST(MAX(created_at) AS VARCHAR) FROM deliveries").fetchall()[0]
    else:
        row = con.sql(f"SELECT COUNT(*) FROM {table}").fetchall()[0]
    return {"rows": int(row[0]), "sha": U.sha([str(x) for x in row])}
    # END SOLUTION


def log_record(step: str, reply, outcome, tables: list[str], verified_by: str) -> dict:
    # BEGIN SOLUTION
    return {"step": step, "request": reply.request, "context_sha": U.sha(reply.context), "model": reply.model,
            "settings": reply.settings, "code": reply.code, "data": {t: fingerprint(t) for t in tables},
            "headline": outcome.headline, "verified_by": verified_by}
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    fp = fingerprint("deliveries")
except NotImplementedError:
    fp = U.fingerprint(con, "deliveries")
print("deliveries:", fp)
U.check(fp["rows"] == U.reference("rows")["deliveries"] and len(fp["sha"]) == 12, "the fingerprint has the planted row count and a 12-character hash")
again = con.sql("SELECT COUNT(*) FROM deliveries").fetchall()[0][0]
U.check(again == fp["rows"], "computing it twice gives the same rows")

# %% [markdown]
# ## 3 · Run one analysis through the logger and check the log
#
# The step is the monthly on-time rate of Lab 1.3 (its second, corrected reply). It is run, checked with
# the three acceptance checks, logged, and then rerun from the log line alone.

# %%
reply = U.recorded("1.3", "brief_v2")
out = U.run_reply(reply, con)
passed = [U.reference_check(c, out.result, con)[0] for c in ("check_total", "check_months", "check_rates")]
verified = f"three acceptance checks passed ({sum(passed)} of 3): total, months, rates"
try:
    record = log_record("monthly_rate", reply, out, ["deliveries", "customers"], verified)
except NotImplementedError:
    record = U.log_record("monthly_rate", reply, out, ["deliveries", "customers"], con, verified_by=verified)

log_dir = U.ART / "lab_3_2"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "run_log.jsonl"
log_path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
print({k: (v if k != "code" else v[:60] + " ...") for k, v in record.items()})
U.check(U.log_gaps(record) == [], "the record lacks nothing a rerun needs")

# Rerun from the log alone: read the line back, run its code, compare
line = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
rerun = U.run_reply(U.reply_from(line), con)
U.check(rerun.headline == line["headline"], f"the rerun reaches the logged headline: {rerun.headline}")
try:
    same_data = all(fingerprint(t) == f for t, f in line["data"].items())
except NotImplementedError:
    same_data = all(U.fingerprint(con, t) == f for t, f in line["data"].items())
U.check(same_data, "and the data has the fingerprint the log recorded")

# %% [markdown]
# **Look at** what the log line holds and what it does not. It holds the request, the model and its
# settings, the code and a fingerprint. It holds no row of data and no key. A log is published with the
# package: it must be safe to publish.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"A log record for the monthly on-time step: request, model, settings, code, fingerprints of two tables and the headline {record['headline']}.",
        checked="U.log_gaps on the record, then a rerun from the log line alone: same headline, same data fingerprint.",
        wrong=f"Nothing in my record. The old log could not be rerun: its three records lacked {sum(len(U.log_gaps(r)) for r in old)} fields between them, among them settings, code and every data fingerprint.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["3.2"]
note = U.note("3.2", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Register a copy of `hubs` with one capacity changed (`con.sql("CREATE TEMP TABLE hubs2 AS SELECT ...")`)
# and fingerprint both with `U.fingerprint(con, "hubs")`, which hashes every column. Does a row count
# alone notice the change?
#
# ## Check yourself
#
# 1. Why does the log record the temperature when the code is logged anyway?
# 2. What does a data fingerprint tell a peer who reruns your step and gets another number?
# 3. Name two things that must never be in a log that is published with a package.
#
# <details><summary>Answers</summary>
#
# 1. The code is what one run produced. To repeat the variability measurement, or to explain why a later
#    run wrote different code, a peer needs the model and its settings.
# 2. Whether the data changed. Same fingerprint and another number: the code or the environment differs.
#    Another fingerprint: the data did.
# 3. Rows or example values of Restricted data, and keys or tokens.
#
# </details>
#
# ## Carry forward
#
# `artifacts/lab_3_2/run_log.jsonl` has the shape of the capstone's log. Lab 3.3 reruns a supplied one.
