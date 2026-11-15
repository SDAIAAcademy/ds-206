# %% [markdown]
# # Lab 2.4 · Five runs of one request
#
# Day 2 · Session 4 (Ask it twice) · 25 min.
#
# One request, one context file, one dataset, one model, the same settings, five runs. You tabulate what
# each run chose and found, measure how alike the code is, and decide which conclusions held in every run.
#
# **AI policy for this lab:** AI-full.
#
# **Tasks**
# - [ ] 1 · Run five replies to one fixed request (5 min)
# - [ ] 2 · Tabulate choices, code and numbers per run (8 min)
# - [ ] 3 · Decide which conclusions held in every run (8 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Run the request five times live at temperature 0 and compare

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
# ## 1 · Run five replies to one fixed request
#
# The five recorded replies answer the same request with the same settings. With a key, the lab also
# sends the request live (twice in quick mode, five times otherwise) so you can see your own model vary.

# %%
runs = U.recorded("2.4")
first = runs["run_1"]
print("request :", first.request)
print("context :", first.context, "| model:", first.model, "| settings:", first.settings, "\n")
U.check(len({(r.request, r.context, r.model, str(r.settings)) for r in runs.values()}) == 1, "all five runs share request, context, model and settings")
outs = {name: U.run_reply(r, con) for name, r in runs.items()}
for name, r in runs.items():
    print(f"{name}: {r.text}")

live = [U.ask(first.request, c=con, temperature=0.7) for _ in range(U.pick(5, 2))] if U.has_key() else []
for i, r in enumerate(x for x in live if x):
    o = U.run_reply(r, con)
    print(f"live {i + 1}:", o.error or o.headline)

# %% [markdown]
# **Look at** the five sentences. Four name Dammam, one names Riyadh. Two say every city got worse.
# If you had asked once, you would hold one of these five, and you would not know which.

# %% [markdown]
# ## 2 · Tabulate choices, code and numbers per run
#
# Each reply's code sets `result` (one row per city: `city`, `before`, `since`, `worse`) and `headline`
# (`worst_city`, `measure`).
#
# ✏️ **Exercise** · Return one row per run, indexed by run name, with: `measure` and `worst_city` from the
# headline; `dammam_since`, the value of `since` for Dammam; `cities_worse`, how many cities the run marks
# as worse; and `code_like_run_1`, `U.similarity` of the run's code to the first run's.

# %%
def tabulate(runs: dict, outs: dict) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for name, r in runs.items():
        res = outs[name].result.set_index("city")
        rows.append({"run": name, "measure": outs[name].headline["measure"], "worst_city": outs[name].headline["worst_city"],
                     "dammam_since": round(float(res.since["Dammam"]), 4), "cities_worse": int(res.worse.sum()),
                     "code_like_run_1": U.similarity(r.code, runs["run_1"].code)})
    return pd.DataFrame(rows).set_index("run")
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    table = tabulate(runs, outs)
except NotImplementedError:
    table = pd.DataFrame(U.load("reference/lab_2_4_table.json")).set_index("run")
U.keep("lab_2_4_table.json", table.reset_index().to_dict("records"))
print(table.to_string())
rates = table[table.dammam_since < 1].dammam_since
print(f"\nDammam's on-time rate since July, in the {len(rates)} runs that report a rate: {rates.min():.4f} to {rates.max():.4f}")
U.check(table.measure.nunique() == 5, "five runs, five different measures")
U.check(table.worst_city.value_counts().to_dict() == {"Dammam": 4, "Riyadh": 1}, "four runs name Dammam, one names Riyadh")

# %% [markdown]
# ## 3 · Decide which conclusions held in every run
#
# Three conclusions a report could draw. A conclusion that held in every run is robust to the choices the
# assistant varies. One that held in some runs depends on a choice, and the `measure` column says which.
#
# ✏️ **Exercise** · Return a dict: conclusion to the number of runs (0 to 5) that support it, for
# `"Dammam is the worst city since July"`, `"Dammam got worse"` and `"No other city got worse"`.

# %%
CONCLUSIONS = ["Dammam is the worst city since July", "Dammam got worse", "No other city got worse"]


def held(outs: dict) -> dict:
    # BEGIN SOLUTION
    count = dict.fromkeys(CONCLUSIONS, 0)
    for o in outs.values():
        res = o.result.set_index("city")
        count[CONCLUSIONS[0]] += o.headline["worst_city"] == "Dammam"
        count[CONCLUSIONS[1]] += bool(res.worse["Dammam"])
        count[CONCLUSIONS[2]] += not res.worse.drop("Dammam").any()
    return {k: int(v) for k, v in count.items()}
    # END SOLUTION

# %%
# Check, with a safety net
try:
    support = held(outs)
except NotImplementedError:
    support = U.load("reference/lab_2_4_held.json")
U.keep("lab_2_4_held.json", support)
variability = pd.DataFrame({"runs_supporting": support})
variability["held_in_every_run"] = variability.runs_supporting == len(runs)
print(variability.to_string())
U.check(list(variability.runs_supporting) == [4, 5, 3], "the three conclusions are supported by 4, 5 and 3 of the 5 runs")

# The runs that disagree are not a vote: read why they disagree, against definitions.md
print()
for name in table.index[(table.worst_city != "Dammam") | (table.cities_worse > 1)]:
    print(f"{name} departs because of its measure: {table.measure[name]}")
truth = U.reference("on_time_by_city")
print("\nplanted on-time rate by city, whole year:", truth)

# %% [markdown]
# **Look at** the two runs that departed. One counted late parcels (a growing company has more of
# everything), one used the system flag (two definitions). Both broke a rule the context file states.
# Variability did not tell you the answer. It told you where to look, in five minutes.
#
# Report "Dammam got worse" as found. Report the other two only after verifying the run you keep, the way
# Lab 2.1 did.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced=f"Five replies to one request with the same context, model and settings: five different measures, code similarity to the first run from {table.code_like_run_1.min()} to 1.0.",
        checked="Ran all five on the data, tabulated measure, worst city, Dammam's value and cities marked worse, and counted the runs supporting each of three conclusions.",
        wrong=(f"Only 'Dammam got worse' held in all five; 'Dammam is worst' held in {support[CONCLUSIONS[0]]} and 'no other city got worse' in {support[CONCLUSIONS[2]]}. "
               "The departing runs counted late parcels or used the system flag, against the context file."),
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["2.4"]
note = U.note("2.4", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# With a key: send the request five times with `temperature=0` and tabulate the replies the same way
# (`U.ask(first.request, c=con, temperature=0)`). Are the five codes identical? Are the numbers?
# What does a hosted model's documentation say about a fixed seed?
#
# ## Check yourself
#
# 1. Five runs gave the same number. What have you learned, and what have you not?
# 2. A conclusion held in three of five runs. Is it 60% true?
# 3. Why does the table record the model and its settings?
#
# <details><summary>Answers</summary>
#
# 1. That the number is stable under this model's variation. Not that it is right: five runs can share
#    one wrong reading of the question. Stability is not verification.
# 2. No. It depends on an analytic choice, and the choice is either right or wrong under the definitions.
#    Find the choice, then check it.
# 3. Variability belongs to a model at given settings. Without them nobody can repeat the measurement,
#    and a later, different result cannot be explained.
#
# </details>
#
# ## Carry forward
#
# The variability table is the evidence of the fourth course outcome, and a required file of the capstone.
