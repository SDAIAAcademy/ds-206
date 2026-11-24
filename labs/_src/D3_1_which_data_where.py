# %% [markdown]
# # Lab 3.1 · Hosted, local or neither
#
# Day 3 · Session 1 (Which data may go where) · 25 min.
#
# Before the first request of a project, every table gets a level and a destination. You apply Hudhud's
# assistant policy to eight tables and two aggregates, prove one decision on the data, and write the
# guard that runs before any prompt leaves the notebook.
#
# All data in this course is synthetic and describes nobody. In this lab you treat it as if it were real.
#
# **AI policy for this lab:** AI-off. The decisions are the analyst's, under the policy.
#
# **Tasks**
# - [ ] 1 · Read the assistant policy and the table catalogue (5 min)
# - [ ] 2 · Classify each table and choose its destination (8 min)
# - [ ] 3 · Find the personal data in the complaint texts (4 min)
# - [ ] 4 · Write the guard and test it (4 min)
# - [ ] 5 · Write the verification note (4 min)
# - [ ] ✱ Stretch · Screen the local assistant's replies on ten known cases, or build a Public aggregate of complaints

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
# ## 1 · Read the assistant policy and the table catalogue
#
# The policy has eight rules, P-1 to P-8. The catalogue lists each table's columns with the kind of
# information each column holds, as recorded by the table's owner.

# %%
print(U.load("docs/assistant_policy.md"))
catalog = U.load("catalog.json")
for item in catalog:
    kinds = sorted(set(item["columns"].values()) - {"operational"})
    print(f"{item['name']:36s} owner: {item['owner']:17s} published: {item['published']!s:5s} other than operational: {', '.join(kinds) or 'nothing'}")

# %% [markdown]
# ## 2 · Classify each table and choose its destination
#
# The kinds of column are: `operational`, `commercial`, `employment`, `contact`, `name`,
# `location of a person`, `free text by a person` and `government id`.
#
# ✏️ **Exercise** · Write the two rules as functions.
# `classify(item)` returns `(level, personal)`: `personal` is `True` when any column is of a kind that
# identifies or describes a person (every kind except `operational` and `commercial`); `level` is
# `"Public"` for a published table, and for an aggregate with no personal column and no cell under 20
# (P-3), otherwise `"Restricted"` (P-1, P-2).
# `destination(item)` returns `"neither"` for a table with a government identity number (P-7), `"hosted"`
# for a Public one (P-4), otherwise `"local"` (P-6).

# %%
PERSONAL_KINDS = {"employment", "contact", "name", "location of a person", "free text by a person", "government id"}


def classify(item: dict) -> tuple[str, bool]:
    # BEGIN SOLUTION
    kinds = set(item["columns"].values())
    personal = bool(kinds & PERSONAL_KINDS)
    public = item["published"] or (item["aggregate"] and not personal and (item["min_cell"] or 0) >= 20)
    return ("Public" if public else "Restricted"), personal
    # END SOLUTION


def destination(item: dict) -> str:
    # BEGIN SOLUTION
    if "government id" in item["columns"].values():
        return "neither"
    return "hosted" if classify(item)[0] == "Public" else "local"
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    handling = pd.DataFrame([{"table": i["name"], "level": classify(i)[0], "personal_data": classify(i)[1],
                              "destination": destination(i)} for i in catalog])
except NotImplementedError:
    handling = pd.DataFrame(U.load("reference/handling.json"))
U.keep("handling.json", handling.to_dict("records"))
print(handling.to_string(index=False))
by_dest = handling.groupby("destination")["table"].apply(list).to_dict()
U.check(by_dest["hosted"] == ["hubs", "agg_on_time_by_city_month"], "rows of one table and one aggregate may reach the hosted assistant")
U.check(by_dest["neither"] == ["drivers"], "the drivers table goes to no assistant")
U.check(len(by_dest["local"]) == 7, "seven items stay with the local assistant")
out_dir = U.ART / "lab_3_1"
out_dir.mkdir(parents=True, exist_ok=True)
handling.to_csv(out_dir / "data_handling.csv", index=False)

# %% [markdown]
# **Look at** the two aggregates. One is Public and may leave. The other has a district column and cells of
# four complaints: an aggregate is not safe because it is an aggregate. And look at `deliveries`: the
# course's main table is Restricted. Until now `U.ask` has sent its **schema** only (P-5), never a row.

# %% [markdown]
# ## 3 · Find the personal data in the complaint texts
#
# The catalogue says `complaints.text` is free text by a person. Prove it without reading a single text:
# count the texts that carry a mobile number.
#
# ✏️ **Exercise** · Return the share of complaint texts that contain a Saudi mobile number: `05` followed
# by eight digits (`regexp_matches(text, '05[0-9]{8}')`). Return a number; print no text.

# %%
def phone_share() -> float:
    # BEGIN SOLUTION
    return float(U.one(con, "SELECT AVG(CASE WHEN regexp_matches(text, '05[0-9]{8}') THEN 1.0 ELSE 0.0 END) FROM complaints"))
    # END SOLUTION

# %%
# Check, with a safety net
try:
    share = phone_share()
except NotImplementedError:
    share = U.load("reference/lab_3_1_share.json")["share"]
U.keep("lab_3_1_share.json", {"share": round(share, 4)})
n = int(U.one(con, "SELECT COUNT(*) FROM complaints"))
print(f"{share:.1%} of {n:,} complaint texts carry a mobile number: about {share * n:,.0f} texts.")
print(f"The 500 rows that Lab 2.3's summary read would hold about {share * 500:.0f} of them.")
U.check(0.25 < share < 0.40, "about a third of the texts carry a phone number")

# %% [markdown]
# **Look at** what a pattern can and cannot do. It finds numbers. Names are in the same texts, and no
# pattern lists every name. Masking free text lowers the risk; it does not change the table's level.

# %% [markdown]
# ## 4 · Write the guard and test it
#
# A policy that lives in a document is followed on good days. The guard runs before every request.
#
# ✏️ **Exercise** · `guard(tables, to, what)` raises `PermissionError` with the rule's number when the
# request breaks the policy, and returns `True` otherwise. `to` is `"hosted"` or `"local"`; `what` is
# `"schema"` or `"rows"`. Use the `destination` column of your handling table: the schema of any table may
# go anywhere (P-5); rows go to the hosted assistant only from a `hosted` table (P-4), to the local one
# from a `hosted` or `local` table (P-6), and from a `neither` table nowhere (P-7).

# %%
DEST = dict(zip(handling.table, handling.destination))


def guard(tables: list[str], to: str, what: str) -> bool:
    # BEGIN SOLUTION
    if what == "schema":
        return True
    for t in tables:
        if DEST[t] == "neither":
            raise PermissionError(f"P-7: rows of {t} go to no assistant")
        if to == "hosted" and DEST[t] != "hosted":
            raise PermissionError(f"P-4: rows of {t} are Restricted and may not go to a hosted assistant")
    return True
    # END SOLUTION

# %%
# Check, with a safety net
def blocked(tables, to, what):
    try:
        guard(tables, to, what)
    except PermissionError as e:
        return str(e)
    except NotImplementedError:
        ref = U.load("reference/lab_3_1_guard.json")
        return ref.get(f"{','.join(tables)}|{to}|{what}", "")
    return ""


cases = [(["deliveries", "customers"], "hosted", "schema"), (["hubs"], "hosted", "rows"), (["complaints"], "hosted", "rows"),
         (["complaints"], "local", "rows"), (["drivers"], "local", "rows"), (["agg_on_time_by_city_month"], "hosted", "rows")]
results = {f"{','.join(t)}|{to}|{what}": blocked(t, to, what) for t, to, what in cases}
U.keep("lab_3_1_guard.json", results)
for k, v in results.items():
    print(f"{k:45s} {'BLOCKED  ' + v if v else 'allowed'}")
U.check([bool(v) for v in results.values()] == [False, False, True, False, True, False], "two of the six requests are blocked")
U.check("P-4" in results["complaints|hosted|rows"] and "P-7" in results["drivers|local|rows"], "each refusal names its rule")
print("\nLab 2.3's summary request, 500 complaint texts to a hosted assistant:", results["complaints|hosted|rows"])

# %% [markdown]
# ## 5 · Write the verification note
#
# Nothing was produced by an assistant in this lab. The note records the decision and how it was checked.
#
# ✏️ **Exercise** · Fill the three parts.

# %%
def my_note():
    # BEGIN SOLUTION
    return dict(
        produced="No assistant output: a data-handling table for eight tables and two aggregates, and a guard that enforces it.",
        checked=f"Each row against rules P-1 to P-7 of the assistant policy; the complaint texts by counting phone numbers ({share:.1%} of texts); the guard on six requests.",
        wrong="Nothing in the table. Lab 2.3's summary request would have sent 500 complaint texts to a hosted assistant: the guard blocks it under P-4.",
    )
    # END SOLUTION

# %%
try:
    parts = my_note()
except NotImplementedError:
    parts = U.load("reference/notes.json")["3.1"]
note = U.note("3.1", **parts)

# %% [markdown]
# ## ✱ Stretch
#
# Two options. Do one.
#
# **A · Screen what comes back.** The guard checks what leaves the notebook. Under P-6 the local assistant
# reads complaint rows, so its replies can quote them. Before a reply goes anywhere (a report, the run log,
# the published package), a screen reads it: it masks a mobile number, blocks a reply that
# carries an identity number, and raises an alert for each block. The alert names the reply, the rule and
# how many matches; it never holds the matched value. A screen is trusted when it gives every one of a set
# of known cases its known verdict, the clean ones included.
#
# **B · An aggregate.** Build an aggregate of complaints that could be classified Public under P-3: no
# personal column, no cell under 20. Which grouping columns can you keep? Who would have to approve it?

# %%
import re

known = U.load("recorded/lab_3_1_known.json")  # ten scripted replies of the local assistant, each with its verdict
MOBILE = r"05[0-9]{8}"


def screen_v1(text: str) -> str:
    """The pattern of task 3, used as it is."""
    return "mask" if re.search(MOBILE, text) else "pass"


def tally(verdicts: dict) -> dict:
    return {"right": sum(verdicts[k["id"]] == k["expected"] for k in known),
            "missed": sum(k["expected"] != "pass" and verdicts[k["id"]] == "pass" for k in known),
            "false_alarms": sum(k["expected"] == "pass" and verdicts[k["id"]] != "pass" for k in known)}


v1 = {k["id"]: screen_v1(k["text"]) for k in known}
print(pd.DataFrame({"case": list(v1), "expected": [k["expected"] for k in known], "v1": list(v1.values())}).to_string(index=False))
print("v1 against the known cases:", tally(v1))

# %% [markdown]
# **Look at** the cases v1 lets through and what they share: the same numbers, written another way.
#
# ✏️ **Exercise (stretch A)** · `screen(case, text)` returns `(verdict, text_out, alert)`.
# First make the text comparable: Arabic-Indic digits to Western ones (`str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")`),
# `+966` or `00966` before a 5 read as `0`, and a space or a dash between two digits removed, and nothing
# else (the slash of a date stays). Then an identity number, ten digits starting with 1 or 2
# (`(?<!\d)[12]\d{9}(?!\d)`), blocks the reply: `text_out` is `""` and `alert` is
# `{"reply": case, "rule": "P-7", "found": "identity number", "count": n}`. Otherwise every mobile becomes
# `[mobile]` (verdict `"mask"`), or the reply passes unchanged with no alert.

# %%
def screen(case: str, text: str) -> tuple[str, str, dict | None]:
    # BEGIN SOLUTION
    t = text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    t = re.sub(r"(?:\+|00)966[ -]?(?=5)", "0", t)
    t = re.sub(r"(?<=\d)[ -](?=\d)", "", t)
    ids = re.findall(r"(?<!\d)[12]\d{9}(?!\d)", t)
    if ids:
        return "block", "", {"reply": case, "rule": "P-7", "found": "identity number", "count": len(ids)}
    masked, n = re.subn(MOBILE, "[mobile]", t)
    return ("mask", masked, None) if n else ("pass", text, None)
    # END SOLUTION

# %%
# Check, with a safety net
try:
    screened = {k["id"]: screen(k["id"], k["text"]) for k in known}
except NotImplementedError:
    screened = {c: tuple(v) for c, v in U.load("reference/lab_3_1_screen.json").items()}
U.keep("lab_3_1_screen.json", screened)
verdicts = {c: v[0] for c, v in screened.items()}
alerts = [v[2] for v in screened.values() if v[2]]
print(pd.DataFrame({"case": list(verdicts), "expected": [k["expected"] for k in known], "screen": list(verdicts.values())}).to_string(index=False))
print("screen against the known cases:", tally(verdicts))
for a in alerts:
    print("ALERT", a)
U.check(tally(verdicts)["right"] == len(known), "the screen gives all ten known cases their verdict, the clean ones included")
U.check(len(alerts) == sum(k["expected"] == "block" for k in known), "one alert for each blocked reply")
U.check(not any(re.search(r"\d{8}", str(a)) for a in alerts), "no alert holds the value it found")
U.check(not any(re.search(MOBILE, v[1].replace(" ", "")) for v in screened.values() if v[0] == "mask"), "no masked reply still carries a mobile")

# %% [markdown]
# ## Check yourself
#
# 1. `deliveries` is Restricted, and the labs sent requests about it to a hosted model. Which rule allowed that?
# 2. Why does the drivers table go to no assistant, when a local one never leaves the company?
# 3. A colleague masks the phone numbers in the complaint texts. May the texts go to the hosted assistant now?
# 4. The screen of stretch A blocks a reply that carries an identity number. What does that block tell you
#    about the requests upstream?
#
# <details><summary>Answers</summary>
#
# 1. P-5: only table and column names were sent. No row, sample or example value left the notebook.
# 2. P-7: no analysis needs a government identity number, so the safest handling is that no model reads
#    it. The local assistant gets a view without the column.
# 3. No. The texts still hold names and what a person wrote; the table stays Restricted. Masking lowers
#    the harm of a leak, not the level.
# 4. An identity number can only reach a reply if a request carried the drivers table, which P-7 sends to
#    no assistant. The block stops the leak; the alert sends someone to find the request the guard let through.
#
# </details>
#
# ## Carry forward
#
# `artifacts/lab_3_1/data_handling.csv` is the data-handling table the capstone asks for. Lab 3.4 loads a
# supplied copy.
