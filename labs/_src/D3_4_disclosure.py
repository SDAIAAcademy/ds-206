# %% [markdown]
# # Lab 3.4 · Method, disclosure and the capstone question
#
# Day 3 · Session 4 (Disclosing assistance) · 25 min.
#
# A report that used an assistant says so: which steps, which tool, which data it saw, how each step was
# verified, and who answers for the numbers. You derive that from the package's log, write the paragraph,
# test it against the log, and then choose the question of your capstone.
#
# **AI policy for this lab:** AI-full for drafting. The paragraph is signed by you.
#
# **Tasks**
# - [ ] 1 · List the assisted steps from the log (5 min)
# - [ ] 2 · Write the method and disclosure paragraph (8 min)
# - [ ] 3 · Test the paragraph against the log; write the note (5 min)
# - [ ] 4 · Choose the capstone question and route its tables (7 min)
# - [ ] ✱ Stretch · Rewrite the paragraph in Arabic for an Arabic report

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
# ## 1 · List the assisted steps from the log
#
# The disclosure is written from the log, not from memory. The log is the one of the Dammam package.
#
# ✏️ **Exercise** · `assisted_steps(log)` returns one row per log record: `step`, `mode`, `model`, `sent`
# (what the assistant was shown) and `verified` (`True` when the record has a non-empty `verified_by`).

# %%
log = U.load("packages/dammam_q3/run_log.jsonl")


def assisted_steps(log: list[dict]) -> pd.DataFrame:
    # BEGIN SOLUTION
    return pd.DataFrame([{"step": r["step"], "mode": r["mode"], "model": r["model"], "sent": r["sent"],
                          "verified": bool(r.get("verified_by"))} for r in log])
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    steps = assisted_steps(log)
except NotImplementedError:
    steps = pd.DataFrame(U.load("reference/lab_3_4_steps.json"))
U.keep("lab_3_4_steps.json", steps.to_dict("records"))
print(steps.to_string(index=False))
U.check(len(steps) == 3 and int(steps.verified.sum()) == 2, "three assisted steps, two of them verified")
unverified = list(steps.step[~steps.verified])
print("not verified:", unverified)

# %% [markdown]
# ## 2 · Write the method and disclosure paragraph
#
# First, a draft that was found in the package. `U.disclosure_check` compares a paragraph with the log.

# %%
draft = U.load("docs/disclosure_draft.md").strip()
print(draft, "\n")
for problem in U.disclosure_check(draft, log):
    print(" ✗", problem)

# %% [markdown]
# ✏️ **Exercise** · Return your paragraph, 60 to 150 words. It states: the **tool** (the model named in the
# log), the **steps** it drafted or produced, the **data it saw**, how each step was **verified** (and
# which step was not), and who is **accountable** for the numbers.

# %%
def my_paragraph() -> str:
    # BEGIN SOLUTION
    model = log[0]["model"]
    return (f"Method and disclosure. Three steps of this analysis were drafted by an AI coding assistant ({model}, temperature 0.2): "
            "the quarterly on-time rate for Dammam, the comparison of long and short routes, and the weekly chart. "
            "The assistant was shown table and column names only; no rows and no personal data left the notebook. "
            "The quarterly rate was recomputed in SQL without the assistant and reconciled; the route comparison was checked "
            "with row counts, an anti-join and a stated denominator. The weekly chart was not independently verified and is "
            "illustrative. The definition of on time, the reading of the results and the recommendation are the analyst's, "
            "who is accountable for every number in this report.")
    # END SOLUTION

# %%
# Check, with a safety net
try:
    paragraph = my_paragraph()
except NotImplementedError:
    paragraph = U.load("reference/disclosure.md").strip()
U.keep("disclosure.md", paragraph + "\n")
print(paragraph, f"\n\n{len(paragraph.split())} words")
U.check(60 <= len(paragraph.split()) <= 150, "the paragraph is between 60 and 150 words")

# %% [markdown]
# ## 3 · Test the paragraph against the log; write the note

# %%
problems = U.disclosure_check(paragraph, log)
for problem in problems:
    print(" ✗", problem)
U.check(problems == [], "the paragraph states all five parts and says nothing the log does not support")
U.check(len(U.disclosure_check(draft, log)) >= 4, "the found draft fails on at least four points")

# %% [markdown]
# ✏️ **Exercise** · Fill the three parts of the note. What was "produced" here is the found draft.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced="A two-sentence draft disclosure: 'AI tools were used for minor formatting. All numbers were verified by the analyst.'",
        checked="Listed the assisted steps from the run log and tested the draft and my own paragraph against the log with U.disclosure_check.",
        wrong=f"The draft named no model, called assistance on headline numbers minor, and claimed all numbers verified while {', '.join(unverified)} has no check. My paragraph says which step was not verified.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["3.4"]
note = U.note("3.4", **parts)

# %% [markdown]
# ## 4 · Choose the capstone question and route its tables
#
# Six questions about Hudhud Parcel that this course has not answered. You have two hours tomorrow.
# Before you choose, see which tables each needs and where the policy lets them go.

# %%
import json

questions = json.loads((U.LABS / "capstone" / "questions.json").read_text(encoding="utf-8"))
dest = {r["table"]: r["destination"] for r in U.load("reference/handling.json")}
for qn in questions:
    route = ", ".join(f"{t} → {dest[t]}" for t in qn["tables"])
    print(f"{qn['id']}  {qn['question']}\n     tables: {route}\n")

# %% [markdown]
# ✏️ **Exercise** · Return `(question_id, reason, kept_step)`: the id of your question, one sentence on why
# you can answer it in two hours, and the one step you will keep for yourself. To propose your own
# question, return `"OWN"` as the id and state the question in the reason; your trainer approves it.

# %%
def my_choice():
    # BEGIN SOLUTION
    return ("Q1", "It needs deliveries and customers only, the measure is one rate with a clear denominator, and I can recompute it in SQL in ten minutes.",
            "Deciding what counts as a second attempt and out of which parcels")
    # END SOLUTION

# %%
try:
    qid, reason, kept = my_choice()
except NotImplementedError:
    qid, reason, kept = U.load("reference/lab_3_4_choice.json")
U.keep("lab_3_4_choice.json", [qid, reason, kept])
ids = {qn["id"] for qn in questions} | {"OWN"}
U.check(qid in ids and len(reason.split()) >= 8 and len(kept.split()) >= 4, f"capstone question {qid} chosen, with a reason and a kept step")
chosen = next((qn for qn in questions if qn["id"] == qid), {"id": "OWN", "question": reason, "tables": []})
plan = {"question": chosen, "reason": reason, "kept_step": kept,
        "hosted_rows_allowed": [t for t in chosen["tables"] if dest[t] == "hosted"],
        "schema_only_to_hosted": [t for t in chosen["tables"] if dest[t] != "hosted"]}
out_dir = U.ART / "capstone"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "choice.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(plan, indent=1, ensure_ascii=False))

# %% [markdown]
# **Look at** `schema_only_to_hosted`. For every question, the hosted assistant may see column names and
# nothing else. Your capstone's data-handling table says so, and your transcripts must show it.
#
# ## ✱ Stretch
#
# Rewrite your paragraph in Arabic for an Arabic report. Keep the model's name and the step names as they
# are in the log, so a reader can match the paragraph to the log.
#
# ## Check yourself
#
# 1. "AI was used in this analysis." Why is that not a disclosure?
# 2. Your log shows one unverified step. What are your two honest options?
# 3. Who is accountable for a number the assistant computed and you verified?
#
# <details><summary>Answers</summary>
#
# 1. A reader cannot tell which numbers it touched, what it saw or how they were checked. A disclosure
#    lets a reader decide how much to rely on each part.
# 2. Verify it before the report goes out, or say in the report that it was not verified.
# 3. You are. Verification is how you earn the right to sign it; the assistant signs nothing.
#
# </details>
#
# ## Carry forward
#
# `artifacts/capstone/choice.json` holds your question. Tomorrow starts from `labs/capstone/`, the
# starter of the package.
