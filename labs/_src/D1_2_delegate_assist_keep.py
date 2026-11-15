# %% [markdown]
# # Lab 1.2 · Delegate, assist or keep
#
# Day 1 · Session 2 (Delegate, assist or keep) · 25 min.
#
# You sort the ten steps of the late-delivery plan into three modes, with a reason for each, and score
# your marks against the analytics lead's. Then you write the three-question rule as a function and see
# where a rule and a person disagree.
#
# **AI policy for this lab:** AI-off for the marking. The judgement is the exercise.
#
# **Tasks**
# - [ ] 1 · Read the plan and the three questions (5 min)
# - [ ] 2 · Mark the ten steps, with a reason each (9 min)
# - [ ] 3 · Write the rule as a function and compare (7 min)
# - [ ] 4 · Write the verification note: the check for each delegated step (4 min)
# - [ ] ✱ Stretch · Sort the steps of an analysis you did last month

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
# ## 1 · Read the plan and the three questions
#
# - **delegate**: the assistant does the step; you check the result.
# - **assist**: the assistant drafts; you do the part that decides the number, or you recompute it.
# - **keep**: you do it. The assistant may be asked to criticise, never to decide.
#
# Three questions sort most steps: is the result **cheap to check**? Is **judgement the product**?
# Are the **stakes high** if it is wrong and nobody notices?

# %%
plan = U.load("plan.json")
print(plan["question"], "\n")
steps = pd.DataFrame(plan["steps"]).set_index("id")
print(steps.to_string())

# %% [markdown]
# ## 2 · Mark the ten steps
#
# ✏️ **Exercise** · Return a dict: step id to `(mode, reason)`. The mode is `"delegate"`, `"assist"` or
# `"keep"`. The reason is one sentence that names what would go wrong, or why it would not.

# %%
def my_marks():
    # BEGIN SOLUTION
    return {
        1: ("keep", "The definition decides every later number and the director will ask why it was chosen"),
        2: ("delegate", "Profiling code has a known right answer and a wrong count shows against the source system"),
        3: ("assist", "The assistant drafts the filters and I check how many rows each one removed"),
        4: ("assist", "It is the headline number, so I recompute it another way before anyone sees it"),
        5: ("delegate", "The table is already checked and a wrong chart shows when I read its axes"),
        6: ("assist", "The join can fan out, so I check row counts and denominators myself"),
        7: ("keep", "Cause against coincidence is a judgement no query settles, and I sign it"),
        8: ("assist", "A summary can misstate one city or language, so I check each sentence against counts"),
        9: ("delegate", "Tidying changes no number and I read the diff in a minute"),
        10: ("keep", "The recommendation is mine to make and to defend in front of the board"),
    }
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
key = {int(k): tuple(v) for k, v in U.load("reference/plan_key.json").items()}
try:
    marks = my_marks()
except NotImplementedError:
    marks = key
U.check(set(marks) == set(range(1, 11)), "all ten steps are marked")
U.check(all(m in ("delegate", "assist", "keep") and len(r.split()) >= 6 for m, r in marks.values()),
        "every mark has a mode and a reason of at least six words")
score = pd.DataFrame({"step": steps["step"].str.slice(0, 58), "yours": {k: v[0] for k, v in marks.items()},
                      "reference": {k: v[0] for k, v in key.items()}})
score["match"] = score.yours == score.reference
print(score.to_string())
matches = int(score.match.sum())
U.check(matches >= 8, f"{matches} of 10 match the reference (the course outcome asks for 8)")
for k in score.index[~score.match]:
    print(f"\nStep {k}: you said {marks[k][0]} because: {marks[k][1]}\n  reference says {key[k][0]} because: {key[k][1]}")

# %% [markdown]
# **Look at** any step where you differ. A different mark with a better reason is not an error: say the
# reason aloud to your neighbour. The reference is one experienced analyst's view, not a law.

# %% [markdown]
# ## 3 · Write the rule as a function
#
# ✏️ **Exercise** · `suggest(step)` returns a mode from the step's three attributes: keep when judgement is
# the product; delegate when the result is cheap to check and the stakes are not high; assist otherwise.

# %%
def suggest(step: dict) -> str:
    # BEGIN SOLUTION
    if step["judgement_is_the_product"]:
        return "keep"
    if step["cheap_to_check"] and not step["high_stakes"]:
        return "delegate"
    return "assist"
    # END SOLUTION

# %%
# Check, with a safety net
try:
    rule = {s["id"]: suggest(s) for s in plan["steps"]}
except NotImplementedError:
    rule = {k: v[0] for k, v in key.items()}
agree = sum(rule[k] == key[k][0] for k in key)
counts = pd.Series(rule).value_counts().to_dict()
print("rule:", rule)
U.check(agree == 10, f"the rule reproduces the reference on {agree} of 10 steps")
U.check(counts == {"assist": 4, "delegate": 3, "keep": 3}, f"four assisted, three delegated, three kept: {counts}")

# %% [markdown]
# **Look at** what the rule needed as input. Someone had to decide, per step, whether the result is cheap
# to check and whether the stakes are high. The rule moved the judgement; it did not remove it.
# Set `high_stakes` of step 8 to `True` in your head: Lab 2.3 shows why some analysts would.

# %% [markdown]
# ## 4 · Write the verification note
#
# For a planning lab the note looks forward: nothing has been produced yet, so "checked" is the check you
# commit to for each delegated step.
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced="Nothing yet: a plan of ten steps, three delegated (2, 5, 9), four assisted (3, 4, 6, 8) and three kept (1, 7, 10).",
        checked="Step 2 against the source system's row counts, step 5 by reading axes against the checked table, step 9 by reading the diff; assisted steps by recomputation.",
        wrong=f"My marks matched the reference on {matches} of 10 steps; the definition, the causal claim and the recommendation stay with the analyst.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["1.2"]
note = U.note("1.2", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Write the steps of an analysis you finished last month, give each the three attributes, and run
# `suggest` on them. Which step did you delegate that the rule would have kept?
#
# ## Check yourself
#
# 1. Step 4 is cheap to check. Why is it assisted and not delegated?
# 2. What is the difference between "assist" and "delegate, then check"?
# 3. Which of the three kept steps could an assistant still help with, and how?
#
# <details><summary>Answers</summary>
#
# 1. The stakes are high: it is the number the director will quote. Cheap to check means the check will
#    be done, by recomputing, before anyone sees it.
# 2. In "assist" the analyst does the deciding part or an independent recomputation. In "delegate" the
#    check is lighter: a count, a read of the axes, a diff.
# 3. All three: by listing options, arguing the other side or finding holes in a draft. The decision
#    and the signature stay with the analyst.
#
# </details>
#
# ## Carry forward
#
# Steps 3, 4 and 5 of this plan are the three steps Lab 1.3 briefs. It loads the plan itself.
