# %% [markdown]
# # Lab 2.3 · A chart and a summary against the data
#
# Day 2 · Session 3 (Charts and words) · 25 min.
#
# Rafiq drew a chart titled "Riyadh is the problem" and wrote a five-sentence summary of the complaints.
# You recompute the series behind the chart and read its encodings, redraw it from a checked table, and
# then treat each sentence of the summary as a claim with a query.
#
# **AI policy for this lab:** AI-off for the recomputation in task 1.
#
# **Tasks**
# - [ ] 1 · Recompute the charted series and read its encodings (8 min)
# - [ ] 2 · Redraw the chart from the checked table (4 min)
# - [ ] 3 · Test each sentence of the complaint summary (9 min)
# - [ ] 4 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Compute complaints per 1,000 parcels by city and language

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
# ## 1 · Recompute the charted series and read its encodings
#
# The request was "Chart late deliveries since July for Riyadh and Dammam." The reply's code builds a
# weekly table and a chart specification. `U.draw` draws exactly what the specification says.

# %%
chart = U.recorded("2.3", "chart")
U.show(chart)
space = {"con": con, "pd": pd}
exec(chart.code, space)                    # the reply's code, as U.run_reply runs it; we also want its chart spec
theirs, spec = space["result"], space["chart"]
print("\nchart spec:", spec)
U.draw(theirs, spec, "lab_2_3_rafiq")
print(theirs.pivot(index="week", columns="city", values="late_deliveries").to_string())

# %% [markdown]
# Three encodings to read on any chart: **what is measured** (the y column), **where the axis starts**, and
# **which periods are complete**.
#
# ✏️ **Exercise** · Return a weekly table for Riyadh and Dammam since 1 July 2026 with `week` (the Monday,
# as a date), `city`, `days` (distinct days of `created_at` in that week), `dispatched`, `late` and
# `late_rate`: D-2, dispatched parcels, no test shipments.

# %%
def weekly_rates() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, """
        SELECT CAST(date_trunc('week', d.created_at) AS DATE) AS week, d.city,
               COUNT(DISTINCT CAST(d.created_at AS DATE)) AS days,
               COUNT(*) AS dispatched,
               SUM(CASE WHEN d.delivered_at <= d.promised_by THEN 0 ELSE 1 END) AS late,
               AVG(CASE WHEN d.delivered_at <= d.promised_by THEN 0.0 ELSE 1.0 END) AS late_rate
        FROM deliveries d
        JOIN customers c ON c.customer_id = d.customer_id
        WHERE d.created_at >= DATE '2026-07-01' AND d.city IN ('Riyadh', 'Dammam')
          AND c.segment <> 'TEST' AND d.status <> 'cancelled'
        GROUP BY ALL ORDER BY week, d.city""")
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    weekly = weekly_rates()
except NotImplementedError:
    weekly = pd.DataFrame(U.load("reference/lab_2_3_weekly.json"))
    weekly["week"] = pd.to_datetime(weekly["week"])
U.keep("lab_2_3_weekly.json", weekly.assign(week=weekly.week.astype(str)).to_dict("records"))
full = weekly[weekly.days == 7]
by_city = full.groupby("city").agg(late_per_week=("late", "mean"), late_rate=("late_rate", "mean")).round(4)
print(by_city.to_string())
partial = sorted(weekly[weekly.days < 7].week.astype(str).str.slice(0, 10).unique())
findings = {
    "measure": f"the chart plots counts: Riyadh has {by_city.late_per_week['Riyadh']:.0f} late parcels a week against {by_city.late_per_week['Dammam']:.0f}, "
               f"but a late rate of {by_city.late_rate['Riyadh']:.3f} against Dammam's {by_city.late_rate['Dammam']:.3f}",
    "axis": f"the y axis starts at {spec['ylim'][0]}, not at 0",
    "window": f"the first and last weeks are partial ({', '.join(partial)}): the 'sharp fall' at the end is {int(weekly[weekly.week == weekly.week.max()].days.iloc[0])} days of data",
}
for k, v in findings.items():
    print(f"{k:8s} {v}")
U.check(by_city.late_per_week["Riyadh"] > by_city.late_per_week["Dammam"], "by count, Riyadh is higher")
U.check(by_city.late_rate["Dammam"] > by_city.late_rate["Riyadh"] + 0.05, "by rate, Dammam is more than five points worse")
U.check(len(partial) == 2, "two weeks of the chart are partial")

# %% [markdown]
# ## 2 · Redraw the chart from the checked table
#
# ✏️ **Exercise** · Return `(table, spec)` for an honest version: complete weeks only, the late **rate** on
# the y axis, the axis from 0, and a title that states what the chart shows.

# %%
def honest():
    # BEGIN SOLUTION
    table = weekly[weekly.days == 7]
    spec = {"kind": "line", "x": "week", "y": "late_rate", "series": "city", "ylim": [0, 0.4],
            "title": "Share of dispatched parcels delivered late, complete weeks since July 2026"}
    return table, spec
    # END SOLUTION

# %%
# Check, with a safety net
try:
    table2, spec2 = honest()
except NotImplementedError:
    table2 = weekly[weekly.days == 7]
    spec2 = U.load("reference/lab_2_3_spec.json")
U.keep("lab_2_3_spec.json", spec2)
ax = U.draw(table2, spec2, "lab_2_3_honest")
U.check(spec2["y"] == "late_rate" and spec2["ylim"][0] == 0 and (table2.days == 7).all(), "rates, an axis from zero, complete weeks only")

# %% [markdown]
# **Look at** both pictures in `artifacts/charts/`. Same data, same weeks, opposite message. The first was
# not a lie: every point on it is a correct count. The title drew a conclusion the encoding could not carry.

# %% [markdown]
# ## 3 · Test each sentence of the complaint summary
#
# The request was "Summarise what customers complain about, by city and language." Read the code before
# the words: it shows what the summary was written from.

# %%
summary = U.recorded("2.3", "summary")
U.show(summary)
sout = U.run_reply(summary, con)
print("\nheadline:", sout.headline)
import re
claims = [c.strip() for c in re.split(r"\s*\d\.\s+", summary.text) if c.strip()]
for i, c in enumerate(claims, 1):
    print(i, c)

# %% [markdown]
# The summary was written from the first 500 rows of an export that is sorted by channel, email first.
# The labels in the `category` column were chosen by care agents for all 20,000 complaints: they are the
# ground truth to test against. No complaint text is printed in this lab.
#
# ✏️ **Exercise** · Write two queries over **all** complaints: `category_shares()` returns `category`,
# `complaints`, `share`; `by_language()` returns `language`, `complaints`, `late_share`, `damaged_share`.

# %%
def category_shares() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, """SELECT category, COUNT(*) AS complaints, COUNT(*) / SUM(COUNT(*)) OVER () AS share
                       FROM complaints GROUP BY category ORDER BY complaints DESC""")
    # END SOLUTION


def by_language() -> pd.DataFrame:
    # BEGIN SOLUTION
    return U.q(con, """SELECT language, COUNT(*) AS complaints,
                              AVG(CASE WHEN category = 'late' THEN 1.0 ELSE 0.0 END) AS late_share,
                              AVG(CASE WHEN category = 'damaged' THEN 1.0 ELSE 0.0 END) AS damaged_share
                       FROM complaints GROUP BY language ORDER BY language""")
    # END SOLUTION

# %%
# Check, with a safety net; the two tables below are supplied
try:
    cats, langs = category_shares(), by_language()
except NotImplementedError:
    ref = U.load("reference/lab_2_3_tables.json")
    cats, langs = pd.DataFrame(ref["cats"]), pd.DataFrame(ref["langs"])
U.keep("lab_2_3_tables.json", {"cats": cats.to_dict("records"), "langs": langs.to_dict("records")})
per_city = U.q(con, """
    WITH parcels AS (SELECT d.city, COUNT(*) AS dispatched FROM deliveries d JOIN customers c ON c.customer_id = d.customer_id
                     WHERE c.segment <> 'TEST' AND d.status <> 'cancelled' GROUP BY d.city)
    SELECT k.city, COUNT(*) AS complaints, ROUND(COUNT(*) * 1000.0 / ANY_VALUE(p.dispatched), 1) AS per_1000_parcels
    FROM complaints k JOIN parcels p ON p.city = k.city GROUP BY k.city ORDER BY complaints""")
dammam = U.q(con, """
    SELECT since_july, late_complaints, ROUND(late_complaints / CASE WHEN since_july THEN 3.0 ELSE 9.0 END, 0) AS per_month
    FROM (SELECT created_date >= DATE '2026-07-01' AS since_july, COUNT(*) AS late_complaints
          FROM complaints WHERE city = 'Dammam' AND category = 'late' GROUP BY 1)
    ORDER BY since_july""")
for t in (cats.round(3), langs.round(3), per_city, dammam):
    print(t.to_string(index=False), "\n")
planted = U.reference("complaints_by_category")
U.check(dict(zip(cats.category, cats.complaints.astype(int))) == planted, "your category counts equal the planted answers")

# %% [markdown]
# ✏️ **Exercise** · Give a verdict per sentence: `True` when the data supports it as written, `False` when
# it does not, with one sentence of evidence that quotes a number from the tables above.

# %%
def verdicts() -> dict:
    # BEGIN SOLUTION
    top = cats.iloc[0]
    lang = langs.set_index("language")
    return {
        1: (False, f"{top.category} is the most common at {top.share:.0%}; damaged is {cats.set_index('category').share['damaged']:.0%}, not half"),
        2: (False, f"{lang.complaints['ar'] / lang.complaints.sum():.0%} of complaints are in Arabic; the sample of 500 was {sout.headline['english_share']:.0%} English"),
        3: (False, f"fewest by count ({int(per_city.complaints.min())}), but the most per 1,000 parcels ({per_city.per_1000_parcels.max()}), so the conclusion does not follow"),
        4: (True, f"late complaints from Dammam went from {int(dammam.per_month[0])} to {int(dammam.per_month[1])} a month"),
        5: (False, f"late is {lang.late_share['ar']:.0%} of Arabic complaints against {lang.late_share['en']:.0%} of English ones; damaged {lang.damaged_share['ar']:.0%} against {lang.damaged_share['en']:.0%}"),
    }
    # END SOLUTION

# %%
# Check, with a safety net
try:
    v = verdicts()
except NotImplementedError:
    v = {int(k): tuple(x) for k, x in U.load("reference/lab_2_3_verdicts.json").items()}
U.keep("lab_2_3_verdicts.json", v)
for i, c in enumerate(claims, 1):
    print(f"{'holds' if v[i][0] else 'FAILS':6s} {i}. {c}\n        {v[i][1]}")
U.check([v[i][0] for i in range(1, 6)] == [False, False, False, True, False], "one of the five sentences holds as written")

# %% [markdown]
# **Look at** who the summary misstated: Madinah, and customers who write in Arabic. Neither was in the
# first 500 rows in any number. And look at the code once more: it read 500 complaint texts, with phone
# numbers and names in them, into a request. Which assistant may see those is Day 3's first question.

# %% [markdown]
# ## 4 · Write the verification note
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced="A weekly chart titled 'Riyadh is the problem' and a five-sentence summary of complaints written from the first 500 rows of the export.",
        checked="Recomputed the weekly series as rates with days per week, read the three encodings, and tested each sentence against category counts, language shares and complaints per 1,000 parcels.",
        wrong=(f"The chart plots counts on an axis from {spec['ylim'][0]} with two partial weeks; by rate Dammam is worse ({by_city.late_rate['Dammam']:.3f} against {by_city.late_rate['Riyadh']:.3f}). "
               f"Four of five sentences fail: the sample was {sout.headline['english_share']:.0%} English email, so Madinah and Arabic complaints were misstated."),
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["2.3"]
note = U.note("2.3", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Compute complaints per 1,000 dispatched parcels by city **and** language. Which group complains most,
# and was it in the 500 rows?
#
# ## Check yourself
#
# 1. Every point of the first chart was a correct count. What was wrong with it?
# 2. Sentence 3 starts with a true statement. Why is its verdict "fails"?
# 3. Why test the summary against the `category` column and not by reading more complaint texts?
#
# <details><summary>Answers</summary>
#
# 1. The measure did not fit the question: counts follow city size. The axis and the partial weeks then
#    exaggerated what was left. The title claimed more than the encoding could support.
# 2. "Fewest complaints" is true by count; "needs the least attention" does not follow, because Madinah
#    has the most complaints per 1,000 parcels. A claim is checked whole.
# 3. The labels cover all 20,000 complaints and can be counted. Reading a few more texts repeats the
#    sampling problem, and the texts carry personal data.
#
# </details>
#
# ## Carry forward
#
# The honest chart is in `artifacts/charts/lab_2_3_honest.png`. Nothing here is needed by Lab 2.4.
