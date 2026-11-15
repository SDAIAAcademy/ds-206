# %% [markdown]
# # Lab 1.4 · A project context file
#
# Day 1 · Session 4 (Context files for a project) · 25 min.
#
# A short request works only when the project has already told the assistant what the words mean. You
# complete the project's context file (`AGENTS.md`), rerun one short brief without it and with it, and
# compare the two outputs on code, numbers and acceptance checks.
#
# **AI policy for this lab:** AI-full.
#
# **Tasks**
# - [ ] 1 · Read the starting context file and find its gaps (4 min)
# - [ ] 2 · Write the three missing sections (8 min)
# - [ ] 3 · Rerun the brief without and with the file; compare (9 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Add the check the remaining error would fail by name

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
# ## 1 · Read the starting context file and find its gaps
#
# The file has a Data section and a Conventions section. `U.context_gaps` names the sections a project
# file for analysis should also have.

# %%
start = U.load("context/AGENTS_start.md")
print(start)
print("missing sections:", U.context_gaps(start))

# %% [markdown]
# ## 2 · Write the three missing sections
#
# ✏️ **Exercise** · Return the text of three sections, each under a `## ` heading: **Definitions** (which
# on-time rule, the denominator, test shipments, the month a parcel belongs to), **Checks** (what the
# assistant must run and show before it answers) and **Do not** (what it must never do). Take the facts
# from `data/docs/definitions.md`; write rules, not explanations.

# %%
def my_sections() -> str:
    # BEGIN SOLUTION
    return """
## Definitions

- On time is D-2 for every month: `delivered_at <= promised_by`. A dispatched parcel never delivered is late.
- Never use `on_time_flag` for a comparison across months: it mixes two definitions.
- The denominator is dispatched parcels: status delivered, failed or returned. Cancelled orders are in no rate.
- Test shipments (customers with segment TEST) are in no rate.
- A parcel belongs to the month of `created_at`.
- All times are local except `scans.scan_time_utc`, which is UTC (local minus three hours).

## Checks

- Before answering, show the row count of the working table and of the result.
- A monthly table has exactly 12 rows, 2025-10 to 2026-09.
- Its deliveries sum to the number of dispatched, non-test parcels.

## Do not

- Do not join `scans` to count parcels: scans can be uploaded twice.
- Do not print rows of `complaints`, `drivers` or `customers`.
- Do not round before the last step.
"""
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    sections = my_sections()
except NotImplementedError:
    sections = U.load("reference/AGENTS_sections.md")
context = start.rstrip() + "\n" + sections
U.keep("AGENTS_sections.md", sections)
U.check(U.context_gaps(context) == [], "the context file has Data, Definitions, Conventions, Checks and Do not")
U.check(all(w in context for w in ("D-2", "TEST", "created_at")), "it names the definition, the test segment and the month rule")
out_dir = U.ART / "lab_1_4"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "AGENTS.md").write_text(context, encoding="utf-8")
print(f"context file: {len(context.split())} words, fingerprint {U.sha(context)}")

# %% [markdown]
# ## 3 · Rerun the brief without and with the file; compare
#
# The brief is one line, the kind written on the second day of a project. It is sent twice: alone, and
# with the context file in front of it. The recorded replies are `no_context` and `with_context`.

# %%
BRIEF = "Monthly on-time rate for Tahani, whole year."
live = U.ask(BRIEF, context=context, c=con)
runs = {name: U.recorded("1.4", name) for name in ("no_context", "with_context")}
outs = {name: U.run_reply(r, con) for name, r in runs.items()}
for name, r in runs.items():
    print(f"\n===== {name}")
    U.show(r)

# %% [markdown]
# ✏️ **Exercise** · `compare(runs, outs)` returns one row per run: the yearly `on_time_rate` from the
# headline, its `gap_points` to the planted answer `U.reference("on_time")` in percentage points, the
# `total` of its deliveries, and how many of the three acceptance checks pass (`U.reference_check(name, result, con)` returns `(passed, saw)` for
# `"check_total"`, `"check_months"` and `"check_rates"`).

# %%
def compare(runs: dict, outs: dict) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for name in runs:
        res = outs[name].result
        passed = [U.reference_check(c, res, con)[0] for c in ("check_total", "check_months", "check_rates")]
        rate = outs[name].headline["on_time_rate"]
        rows.append({"run": name, "on_time_rate": rate, "gap_points": round(abs(rate - U.reference("on_time")) * 100, 1),
                     "total": int(res["deliveries"].sum()), "checks_passed": sum(passed)})
    return pd.DataFrame(rows).set_index("run")
    # END SOLUTION

# %%
# Check, with a safety net
try:
    table = compare(runs, outs)
except NotImplementedError:
    table = pd.DataFrame(U.load("reference/lab_1_4_compare.json")).set_index("run")
print(table.to_string())
U.keep("lab_1_4_compare.json", table.reset_index().to_dict("records"))
print("\ncode similarity of the two replies:", U.similarity(runs["no_context"].code, runs["with_context"].code))
truth = U.reference("on_time")
print(f"planted answer: {truth}")
U.check(table.loc["with_context", "gap_points"] < table.loc["no_context", "gap_points"], "with the context file the number is closer to the planted answer")
U.check(table.loc["with_context", "checks_passed"] < 3, "and one acceptance check still fails with the context file")
for name in runs:
    for c in ("check_total", "check_months", "check_rates"):
        ok, saw = U.reference_check(c, outs[name].result, con)
        print(f"{name:13s} {c:13s} {'pass' if ok else 'FAIL'}  {saw}")
if live:
    lo = U.run_reply(live, con)
    print("\nYour live reply with the context file:", lo.error or lo.headline)

# %% [markdown]
# **Look at** the reply with the context file. It follows D-2, drops tests, takes the month from
# `created_at` and uses local times, as the file says. Find the one word in its `WHERE` clause that still
# breaks the denominator rule. The file told the assistant the rule. Only the check showed that the rule
# was not followed, and "closer" is not a result anyone can sign.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts, with the numbers.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"Two replies to one short brief: {table.loc['no_context', 'on_time_rate']:.4f} without the context file and {table.loc['with_context', 'on_time_rate']:.4f} with it.",
        checked="The three acceptance checks of Lab 1.3 on both results, and a read of each query against definitions.md.",
        wrong=f"Without the file: UTC scans against local promises, tests kept, a join to scans ({table.loc['no_context', 'gap_points']} points off). With it: delivered parcels only, so failed parcels left the denominator ({table.loc['with_context', 'gap_points']} points off); the true rate is {truth}.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["1.4"]
note = U.note("1.4", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# The file already states the denominator rule, and the reply ignored it. Write a fourth acceptance check
# that names this error: the share of failed and returned parcels in the working table is above zero. If you have a key, rerun `U.ask(BRIEF, context=...)` and apply
# the checks to the live reply.
#
# ## Check yourself
#
# 1. The reply with the context file passed more checks. Is the context file a form of verification?
# 2. Which belongs in the context file: the director's question, or the on-time definition?
# 3. Why does the file say "do not join scans to count parcels" when the assistant could remove duplicates?
#
# <details><summary>Answers</summary>
#
# 1. No. It lowers the number of errors made; it finds none. The reply with the file still broke a rule
#    the file states.
# 2. The definition: it holds for every request in the project. The question belongs in the brief.
# 3. A rule that removes the trap is cheaper to check than a repair. Whether duplicates were removed
#    correctly is one more thing to verify.
#
# </details>
#
# ## Carry forward
#
# Your file is in `artifacts/lab_1_4/AGENTS.md`. The capstone starter has the same skeleton.
