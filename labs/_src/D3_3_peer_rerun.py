# %% [markdown]
# # Lab 3.3 · Rerun a supplied package
#
# Day 3 · Session 3 (The peer rerun) · 25 min.
#
# You are Jana Al-Rajhi, the peer. Dareen's package on Dammam claims four headline numbers. You rerun every
# logged step on your own copy of the data, compare with the claims, and trace each number to the step
# that produced it. Two numbers match. One drifted. One has no step at all.
#
# **AI policy for this lab:** AI-off. A rerun follows the log; nothing is asked of an assistant.
#
# **Tasks**
# - [ ] 1 · Read the package's README and its log (4 min)
# - [ ] 2 · Rerun every logged step on your data (8 min)
# - [ ] 3 · Compare with the claimed numbers and trace each one (9 min)
# - [ ] 4 · Write the rerun log as the note (4 min)
# - [ ] ✱ Stretch · Write the missing step and log it so the package passes

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
# ## 1 · Read the package's README and its log
#
# The package is in `data/packages/dammam_q3/`: a README with the headline numbers, `run_log.jsonl`,
# `headline.json` (each number with the step and key it claims to come from) and `notes.md`.

# %%
print(U.load("packages/dammam_q3/README.md"))
log = U.load("packages/dammam_q3/run_log.jsonl")
claims = U.load("packages/dammam_q3/headline.json")
for rec in log:
    print(f"step {rec['seq']} · {rec['step']:16s} mode: {rec['mode']:9s} model: {rec['model']} {rec['settings']} "
          f"| gaps: {U.log_gaps(rec) or 'none'}")

# %% [markdown]
# **Look at** the gaps column before running anything. One step has no `verified_by`. That is not a
# rerun problem; it is a disclosure problem, and Lab 3.4 returns to it.

# %% [markdown]
# ## 2 · Rerun every logged step on your data
#
# ✏️ **Exercise** · `rerun(log)` returns one row per logged step: `step`, `same_data` (every table's
# `U.fingerprint(con, table)` equals the fingerprint in the record), `logged` (the record's headline),
# `rerun` (the headline of `U.run_reply(U.reply_from(record), con)`) and `same` (the two headlines are equal).

# %%
def rerun(log: list[dict]) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for rec in log:
        out = U.run_reply(U.reply_from(rec), con)
        rows.append({"step": rec["step"],
                     "same_data": all(U.fingerprint(con, t) == f for t, f in rec["data"].items()),
                     "logged": rec["headline"], "rerun": out.headline, "same": out.headline == rec["headline"]})
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    result = rerun(log)
except NotImplementedError:
    result = pd.DataFrame(U.load("reference/lab_3_3_rerun.json"))
U.keep("lab_3_3_rerun.json", result.to_dict("records"))
print(result.to_string(index=False))
U.check(bool(result.same_data.all()), "your tables have the fingerprints the package ran on")
U.check(bool(result.same.all()), "all three logged steps rerun to their logged headline")

# %% [markdown]
# Every step reruns. Is the package reproduced? Not yet: a reader quotes the **README**, not the log.

# %% [markdown]
# ## 3 · Compare with the claimed numbers and trace each one
#
# ✏️ **Exercise** · `trace(claims, result)` returns one row per claimed number with `name`, `claimed`,
# `rerun` (the value of the claim's `key` in the rerun headline of its `step`, or `None` when the claim
# names no step) and `status`: `"matched"` when the two agree to three decimals, `"drifted"` when a step
# exists and they differ, `"no step"` when no logged step produces the number.

# %%
def trace(claims: list[dict], result: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    heads = dict(zip(result.step, result.rerun))
    rows = []
    for c in claims:
        got = heads[c["step"]][c["key"]] if c["step"] else None
        status = "no step" if got is None else ("matched" if abs(got - c["value"]) < 0.0005 else "drifted")
        rows.append({"name": c["name"], "claimed": c["value"], "rerun": got, "status": status})
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
# Check, with a safety net
try:
    traced = trace(claims, result)
except NotImplementedError:
    traced = pd.DataFrame(U.load("reference/lab_3_3_trace.json"))
U.keep("lab_3_3_trace.json", traced.astype(object).where(traced.notna(), None).to_dict("records"))
print(traced.to_string(index=False))
U.check(list(traced.status) == ["matched", "matched", "drifted", "no step"], "two numbers match, one drifted, one has no logged step")
drift = traced[traced.status == "drifted"].iloc[0]
print(f"\ndrift: the README says {drift.claimed:.4f}, the logged step gives {drift['rerun']:.4f} ({(drift.claimed - drift['rerun']) * 100:+.2f} points)")

# %% [markdown]
# **Look at** the two failures. They are different. The drifted number has a step: the README was written
# from an earlier run and never updated. The fourth number has none: someone computed it by hand. It may
# even be right (Lab 2.3 found 144 a month). A peer cannot know, and that is the finding.

# %% [markdown]
# ## 4 · Write the rerun log as the note
#
# The peer's rerun log is a verification note about a package. The capstone requires one from your peer.
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"A package with three logged steps and four headline numbers in its README; I reran it as the peer on tables with matching fingerprints.",
        checked="Ran the code of every log line, compared each rerun headline with the logged one, then traced each README number to its step and key.",
        wrong=(f"All three steps rerun. Two README numbers match. The long-route rate drifted: README {drift.claimed:.4f}, log {drift['rerun']:.4f}. "
               "The complaints number has no logged step. One step, weekly_chart, has no verification recorded. Not reproduced until those are fixed."),
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["3.3"]
note = U.note("3.3", **parts)
out_dir = U.ART / "lab_3_3"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "rerun_log.md").write_text(note + "\n" + traced.to_string(index=False) + "\n", encoding="utf-8")

# %% [markdown]
# ## ✱ Stretch
#
# Write the query that produces the fourth number, run it, and build its log record with `U.log_record`
# (you will need a `U.Reply` holding your request and code). Does the package pass `trace` now?
#
# ## Check yourself
#
# 1. Every logged step reran to its logged headline. Why is the package still not reproduced?
# 2. The fourth number is probably right. Why does the peer still fail it?
# 3. What did the fingerprints add to this rerun?
#
# <details><summary>Answers</summary>
#
# 1. Readers quote the README. One of its numbers differs from what the log produces, and one comes from
#    no logged step.
# 2. A peer can only confirm what can be rerun. A number with no step rests on the author's word, which
#    is what a package exists to replace.
# 3. They showed the rerun used the same data. Without them, a different result could not be told apart
#    from different data.
#
# </details>
#
# ## Carry forward
#
# `artifacts/lab_3_3/rerun_log.md` is the shape of the peer rerun log in the capstone. Lab 3.4 writes the
# disclosure paragraph for this same package, from its log.
