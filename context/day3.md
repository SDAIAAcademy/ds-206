---
course: "Analysis with AI Assistants: Delegate, Verify, Reproduce"
code: "DS-206"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-206/slides/day3.html"
---

# Analysis with AI Assistants: Delegate, Verify, Reproduce

## Day 3: Reproduce and disclose

Which table may reach which assistant, what a rerun needs from a log, and what a report says about the assistance

#### [day3#title] Reproduce and disclose

*SDAIA Academy · Analysis with AI Assistants: Delegate, Verify, Reproduce*

Day 3: Which table may reach which assistant, what a rerun needs from a log, and what a report says about the assistance

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-206

#### [day3#agenda] Reproduce and disclose

*Today*

- **Session 1 · Which data may go where**: The classification level of a table and the organisation's assistant policy decide its destination: hosted, local or neither
- **Session 2 · Logging assisted work**: A rerun needs the prompt, the context, the model and its settings, the code, a fingerprint of the data and the output
- **Session 3 · The peer rerun**: A package is reproducible when a peer reaches the same headline numbers from its logs alone, and every reported number has a logged step
- **Session 4 · Disclosing assistance**: A report says which steps were assisted, by what, on which data, how they were verified and who answers for the numbers

#### [day3#check-day2-review] Which check finds which error?

*Review · Day 2*

**Question:** An assisted query reports 91% on time for Madinah in September. Its last line filters `created_at BETWEEN '2026-09-01' AND '2026-09-30'`. Which check shows what that filter did?

- A. An anti-join of the September scope against the query's rows
- B. Rows against distinct parcels after each join
- C. Running the request five times and comparing
- D. Reading the y axis of the chart

### Session 1: Which data may go where

#### [day3#s1] Which data may go where

*Session 1*

- Classify the tables of an analysis by their most sensitive column
- Assign each table to a hosted assistant, a local assistant or neither under a written policy
- Enforce the assignment with a guard that runs before any prompt leaves

#### [day3#levels-in-one-slide] The level decides the destination. Today the unit is a table of your analysis

*What you already know*

- **From Responsible Data and AI Practice (FN-106).**
  - Four national levels: Top Secret, Secret, Restricted, Public
  - The level follows the impact of unauthorised disclosure
  - Generative AI tools: data classified Public only
  - Three destinations: a hosted service, a model you run, or no model
- **What an analysis adds.**
  - Eight tables, joined, each with its own owner
  - An assistant that reads whatever the notebook hands it
  - Results, samples and error messages that travel back into prompts
  - Aggregates you create, which need a level too

#### [day3#a-table-takes-its-highest-column] A table takes the level of its most sensitive column

*Rules P-1 and P-2 of Hudhud's policy*

| Column of `deliveries` | Kind |
| --- | --- |
| `delivery_id`, `status`, `created_at` … | operational |
| `cod_amount` | commercial |
| `district` | *location of a person* |
| `recipient_phone` | *contact* |
| The table | Restricted, personal data |

- Sixteen operational columns do not dilute two personal ones.
- A **commercial** column also makes a table Restricted: a contract rate, a route plan.
- A table nobody has classified is treated as Restricted.
- The **data owner** classifies. The analyst applies and records.

#### [day3#the-data-handling-table] Ten items, three destinations

*Lab 3.1, the reference result*

| Item | Level | Personal | Rows may go to | Item | Level | Personal | Rows may go to |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hubs | Public | no | hosted | deliveries | Restricted | yes | local |
| customers | Restricted | yes | local | scans | Restricted | yes | local |
| drivers | Restricted | yes | neither | complaints | Restricted | yes | local |
| driver_shifts | Restricted | yes | local | on-time by city and month | Public | no | hosted |
| route_plans | Restricted | no | local | complaints by district | Restricted | yes | local |

> **The course's main table is Restricted.** Every request you sent in two days was about `deliveries`. The next slide says why that was allowed.

#### [day3#schema-is-not-rows] The assistant wrote code about data it never saw

*Rule P-5*

- **What left the notebook in every lab.**
  - The request
  - The context file
  - Table and column names with their types
- **What sends rows without your noticing.**
  - "Here are the first five rows, what is wrong?"
  - An error message that quotes a value
  - An example in the context file
  - An agent allowed to run queries and read their output

> **An agent with a database connection reads rows by design.** For Restricted tables that agent is local, or it does not get the connection.

#### [day3#an-aggregate-is-not-automatically-safe] An aggregate is not safe because it is an aggregate

*Rule P-3*

- **On-time rate by city and month.** No personal column. Smallest cell: 3,200 parcels. **Public**, once its owner says so. May go to the hosted assistant.
- **Complaints by district and category.** A district is where a person lives. Smallest cell: 4 complaints. **Restricted.** Four complaints about one driver in one district describe people.

> **Two tests before an aggregate leaves:** no column that locates or describes a person, and no cell built from fewer than 20 parcels. Then the owner classifies it.

#### [day3#free-text-carries-people] A third of the complaint texts carry a phone number

*Lab 3.1, measured*

- **31.5%** of 20,000 complaint texts contain a mobile number: about 6,300 texts
- **155** of them in the 500 texts that the summary of Lab 2.3 read

- A pattern finds numbers. **No pattern lists every name.**
- Masking lowers the harm of a leak. It does not change the table's level.
- Texts written by customers stay on a **local** assistant, or are read by people.
- The labels in `category` can be counted without reading a text.

#### [day3#a-guard-before-every-request] A guard runs before every request, on good days and bad

*From document to code*

```python
# file: Lab 3.1 · guard
def guard(tables, to, what):
    if what == "schema":
        return True                        # P-5
    for t in tables:
        if DEST[t] == "neither":
            raise PermissionError(f"P-7: {t}")
        if to == "hosted" and DEST[t] != "hosted":
            raise PermissionError(f"P-4: {t}")
    return True
```

| Request | Result |
| --- | --- |
| Schema of deliveries, to hosted | allowed |
| Rows of hubs, to hosted | allowed |
| Rows of complaints, to hosted | *blocked, P-4* |
| Rows of complaints, to local | allowed |
| Rows of drivers, to local | *blocked, P-7* |

#### [day3#check-destination] What may the hosted assistant receive?

*Checkpoint*

**Question:** You want a hosted assistant to help explain why split-shift drivers have more failed deliveries. Under Hudhud's policy, what may you send it?

- A. Rows of driver_shifts, since driver_id is not a name
- B. Twenty sample rows of deliveries joined to shifts
- C. The drivers table with names masked
- D. The schema of both tables, and an aggregate its owner classified Public

#### [day3#lab-3-1] Hosted, local or neither

Lab 3.1 · 25 min

Decide which tables a local or a hosted assistant may process, prove one decision on the data and enforce all of them in code.

[D3_1_which_data_where.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D3_1_which_data_where.ipynb)

- [ ] Read the assistant policy and the table catalogue (5 min)
- [ ] Classify each table and choose its destination (8 min)
- [ ] Find the personal data in the complaint texts (4 min)
- [ ] Write the guard and test it (4 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Build an aggregate of complaints that may go to the hosted assistant

### Session 2: Logging assisted work

#### [day3#s2] Logging assisted work

*Session 2*

- List what a log record must hold for a step to be rerun
- Write a log record with a data fingerprint for one assisted step
- Find what an incomplete log lacks before someone else has to

#### [day3#what-a-rerun-needs] A rerun needs nine things from every assisted step

*The run log*

| Field | Why a peer needs it | Field | Why a peer needs it |
| --- | --- | --- | --- |
| **step** | To match it to a number in the report | **code** | The thing that is rerun |
| **request** | Word for word: what was asked | **data** | A fingerprint: was it this data? |
| **context** | A hash of the context file in force | **headline** | What the step produced then |
| **model** | Name and version: services change | **verified by** | The check, or its absence |
| **settings** | Temperature, a seed if supported |  |  |

> **Logged by the notebook, not typed afterwards.** A log written from memory is a story about a log.

#### [day3#a-log-that-cannot-be-rerun] Each line made sense on the day it was written

*Lab 3.2, the supplied log*

| Step | What the log says | What a rerun lacks |
| --- | --- | --- |
| monthly_rate | A request, a query, "the notebook assistant" | Settings, context, data fingerprint, any check |
| by_city | The request is "same but by city" | The code, context, data fingerprint; verified by "looked right" |
| chart | The code is "see notebook cell 14" | The request, the context, the temperature, the data, the headline, any check |

> **"Same but by city" is a request only inside one conversation.** A log line must stand without the lines around it.

#### [day3#fingerprint-the-data] A fingerprint identifies the data without storing it

*Was it this data?*

```python
# file: Lab 3.2 · fingerprint
def fingerprint(table):
    row = con.sql("""
        SELECT COUNT(*), SUM(delivery_id),
               CAST(MIN(created_at) AS VARCHAR),
               CAST(MAX(created_at) AS VARCHAR)
        FROM deliveries""").fetchall()[0]
    return {"rows": int(row[0]),
            "sha": U.sha([str(x) for x in row])}
```

| The peer's rerun gives | Fingerprint | So |
| --- | --- | --- |
| The same number | same | Reproduced |
| Another number | same | The code or the environment differs |
| Another number | different | The data changed: late corrections, a new export |
| The same number | different | Luck. Look again |

#### [day3#one-log-record] One line per step, complete on its own

*Lab 3.2, the record you write*

```json
// file: run_log.jsonl · one line, shown on several
{"step": "monthly_rate",
 "request": "Follow the brief below. Do step 2: the monthly on-time rate.",
 "context_sha": "a699f7c0c555",
 "model": "google/gemma-4-31b-it:free",
 "settings": {"temperature": 0.7},
 "code": "result = con.sql(\"\"\"SELECT strftime(d.created_at, '%Y-%m') AS month, ...",
 "data": {"deliveries": {"rows": 500000, "sha": "..."}, "customers": {"rows": 3005, "sha": "..."}},
 "headline": {"on_time_rate": 0.7942},
 "verified_by": "three acceptance checks passed (3 of 3): total, months, rates"}
```

#### [day3#rerun-from-the-line-alone] Prove the log by rerunning from the line alone

*The test of a log*

1. **1 · Read the line** back from the file, not from memory
2. **2 · Run its code** in a fresh connection
3. **3 · Compare headlines** 0.7942 and 0.7942
4. **4 · Compare fingerprints** the data is the data

> **You are your own first peer.** If you cannot rerun your step from its log line today, nobody will next month.

#### [day3#a-log-is-published] A log must be safe to publish

*The log leaves with the package*

- **In the log.**
  - Requests and replies, as sent
  - Code
  - Fingerprints and headline numbers
  - What was sent: "schema only"
- **Never in the log.**
  - Rows or example values of Restricted data
  - Keys and tokens
  - A transcript in which a row was pasted
  - Outputs that print personal data

> **The capstone repository is public.** Its transcripts are the evidence of how you worked, and of what the assistant was shown.

#### [day3#check-log] What does this log line lack?

*Checkpoint*

**Question:** A log line holds the step name, the full request, the model, temperature 0.2, the code and the headline number. A peer reruns the code and gets a different number. What can the peer not decide?

- A. Whether the model's settings were the same
- B. Whether the data changed or the computation did
- C. Whether the request was the one the report describes
- D. Whether the right code was rerun

#### [day3#lab-3-2] A run log

Lab 3.2 · 25 min

Log prompts, model settings and outputs for one analysis, with a fingerprint of the data it ran on.

[D3_2_run_log.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D3_2_run_log.ipynb)

- [ ] Read an incomplete log and list what a rerun lacks (5 min)
- [ ] Write the log record and the data fingerprint (9 min)
- [ ] Run one analysis through the logger and check the log (7 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Change one row of a table and show that the fingerprint changes

### Session 3: The peer rerun

#### [day3#s3] The peer rerun

*Session 3*

- Rerun a package from its log without asking its author
- Classify each headline number as matched, drifted or without a step
- Write a rerun log that an assessor can read in two minutes

#### [day3#reproduced-means] Reproduced: a peer reaches the headline numbers from the package alone

*A definition*

- **A peer.** Someone who did not do the work and does not share your notebook's memory.
- **The headline numbers.** The ones in the README and the report: what a reader will quote.
- **From the package alone.** The log, the code and the data. No question to the author, no "run cell 14 first".

> **Reproduced is not correct.** A rerun shows that the numbers come from the logged steps. The verification notes are what argue that the steps are right.

#### [day3#anatomy-of-a-package] The package of an assisted analysis

*What is in the repository*

| File | Holds | From |
| --- | --- | --- |
| `README.md` | The question, the headline numbers, the method and disclosure paragraph | Today |
| `brief.md`, `AGENTS.md` | What was delegated and under which rules | Day 1 |
| `run_log.jsonl`, `transcripts/` | Every assisted step, and the conversations as they happened | Today |
| `headline.json` | Each headline number with the step and key it comes from | Today |
| `notes.md`, `variability.md` | A verification note per headline number; five runs of one request | Day 2 |
| `data_handling.md` | Each table's level and destination | Today |
| `rerun_log.md` | Written by the peer, not by you | Today |

#### [day3#three-outcomes-for-a-number] Every headline number ends in one of three states

*Tracing*

- **Matched.** A logged step produces it, and the rerun gives the same value.
- **Drifted.** A logged step claims to produce it, and the rerun gives another value. The text and the code have parted.
- **No step.** Nothing in the log produces it. It was typed, copied or computed somewhere else.

> **Trace from the report backwards.** Start from each number a reader will quote and ask which line of the log made it.

#### [day3#the-rerun-of-the-dammam-package] Three steps rerun. Two of four numbers are reproduced

*Lab 3.3, measured*

| Headline number in the README | Claimed | Rerun | Status |
| --- | --- | --- | --- |
| Dammam on-time rate, third quarter of 2026 | 72.26% | 72.26% | matched |
| Dammam on-time rate, second quarter of 2026 | 79.67% | 79.67% | matched |
| On-time rate on long routes, July to September | 68.41% | 68.05% | *drifted* |
| Late complaints from Dammam per month since July | 144 |  | *no step* |

> **All three logged steps reran to their logged headline, on data with matching fingerprints.** The package is still not reproduced: readers quote the README.

#### [day3#probably-right-is-not-reproduced] The number with no step is probably right. It still fails

*The fourth number*

**144** late-delivery complaints from Dammam per month since July: the value Lab 2.3 also found

- A peer can confirm only what can be rerun.
- A number with no step rests on the author's word, which is what a package exists to replace.
- Next quarter someone updates the package: this number will silently stay 144.
- The repair takes five minutes: write the query, log it.

#### [day3#numbers-in-text-come-from-the-log] Numbers in the text are written by the log, not typed

*Preventing drift*

```json
// file: headline.json · one entry
{"name": "On-time rate on long routes",
 "value": 0.6805,
 "step": "long_short",
 "key": "long"}
```

- Each headline number names its **step** and **key**.
- The README table is generated from this file, after the last run.
- A number with no step cannot be entered.
- A change to a query changes the README in the same commit.

> **Drift is a process problem.** Nobody intends to leave an old number in a README. Remove the typing and the drift goes with it.

#### [day3#the-peers-part] The peer reruns, traces and writes. The author repairs

*How a peer works*

- **The peer.**
  - Uses the package only, and asks nothing
  - Reruns every logged step
  - Traces every headline number
  - Writes a rerun log: what matched, what did not
- **The peer does not.**
  - Fix the package quietly
  - Pass a number because it "looks right"
  - Rerun the request through an assistant
  - Judge the conclusion: that is the review, a different task

#### [day3#check-rerun] Is this package reproduced?

*Checkpoint*

**Question:** A peer reruns a package. Every logged step runs and gives its logged headline. The README's main number, 18.2%, appears in no step's headline; the nearest is 18.9%. What does the rerun log say?

- A. Reproduced: all steps rerun to their logged values
- B. Reproduced within tolerance: 18.2% and 18.9% are close
- C. Not reproduced: the main number does not come from any logged step
- D. Reproduced after the peer corrected the README to 18.9%

#### [day3#lab-3-3] Rerun a supplied package

Lab 3.3 · 25 min

Rerun a supplied package from its logs and check that the numbers match its README.

[D3_3_peer_rerun.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D3_3_peer_rerun.ipynb)

- [ ] Read the package's README and its log (4 min)
- [ ] Rerun every logged step on your data (8 min)
- [ ] Compare with the claimed numbers and trace each one (9 min)
- [ ] Write the rerun log as the note (4 min)
- [ ] ✱ Stretch: Write the missing step and log it so the package passes

### Session 4: Disclosing assistance

#### [day3#s4] Disclosing assistance

*Session 4*

- Derive the assisted steps of an analysis from its log
- Write a method and disclosure paragraph that the log supports
- Choose a capstone question and route its tables before starting

#### [day3#why-a-report-says-so] A disclosure lets the reader decide how much to rely on each part

*Disclosure*

- Which numbers did an assistant touch?
- What was it shown?
- How was each one checked, and which were not?
- Who answers for them?

- **For government entities.** The national guidelines ask them to be transparent about content created with generative AI.
- **For anyone who writes code with it.** The guidelines for the public advise marking generated code as such, and verifying it.

#### [day3#five-parts-of-a-disclosure] Five things, in one paragraph

*What it states*

| Part | The question it answers | From |
| --- | --- | --- |
| **Tool** | Which assistant, which model, which settings? | The log |
| **Steps** | What did it draft or produce? | The log |
| **Data seen** | Schema, aggregates or rows, and of what level? | The data-handling table |
| **Verification** | How was each step checked? Which was not? | The verification notes |
| **Accountability** | Who decided, and who signs? | You |

> **Four of the five are copied from files you already have.** A disclosure is hard to write only when the log does not exist.

#### [day3#the-draft-against-the-log] Two sentences, eight problems

*Lab 3.4, the draft found in the package*

**The draft (weak example):** AI tools were used for minor formatting in this analysis. All numbers were verified by the analyst.

- Names no assistant and no model
- Names no step
- Does not say what the assistant saw
- Does not say who is accountable
- Calls assistance on headline numbers "minor"
- Claims all numbers verified: the chart step has no check

> **The second sentence is false, and the log proves it.** A disclosure that overstates verification is worse than none.

#### [day3#a-paragraph-the-log-supports] A paragraph the log supports

*The reference paragraph*

Prompt for Method and disclosure:

```text
Three steps of this analysis were drafted by an AI coding assistant (rafiq-recorded-1, temperature 0.2):
the quarterly on-time rate for Dammam, the comparison of long and short routes, and the weekly chart.
The assistant was shown table and column names only; no rows and no personal data left the notebook.
The quarterly rate was recomputed in SQL without the assistant and reconciled; the route comparison was checked with row counts, an anti-join and a stated denominator. The weekly chart was not independently verified and is illustrative.
The definition of on time, the reading of the results and the recommendation are the analyst's, who is accountable for every number in this report.
```

#### [day3#an-unverified-step-has-two-honest-options] An unverified step has two honest options

*When the log shows a gap*

- **Verify it before the report goes out.** Recompute the series, read the encodings, write the note. Fifteen minutes for a chart.
- **Say that it was not verified.** Name the step and say how to read it: illustrative, not a source for numbers.

> **There is no third option.** Leaving the step out of the paragraph, or folding it into "all numbers were verified", is the failure the defence looks for.

#### [day3#mark-assisted-code] The repository shows which code was assisted, and how

*Disclosure below the report*

- **In the code.** A header comment on an assisted query: drafted by the assistant, the log step, the check that passed.
- **In the history.** Commits that separate "assistant draft" from "repair after check", so the diff is the verification.
- **In the transcripts.** The conversations as they happened, including the replies that were rejected.

> **The rejected replies are evidence in your favour.** A transcript with no failed check suggests no check was run.

#### [day3#choosing-the-capstone-question] Choose a question you can verify in two hours

*Tomorrow*

1. Cash on delivery and second attempts, by city
2. Split shifts and failed deliveries
3. Express against standard, each on its own cut-off
4. Complaint categories after late and after on-time parcels
5. Replanned routes against routes planned once
6. Failed and returned parcels by merchant segment

- **Before you choose.** Which tables does it need, and where may they go? What is the one rate, and out of what? Which step will you keep?
- **A smaller question, fully verified.** scores above a larger one with a headline nobody recomputed. The rubric gives verification 30 of 100.

#### [day3#check-disclosure] Which disclosure is honest?

*Checkpoint*

**Question:** A log shows two assisted steps: a rate that was recomputed by hand, and a summary of complaint categories that was not checked. Which sentence belongs in the report?

- A. The rate was recomputed without the assistant; the summary was not verified and is indicative
- B. All assisted results were verified by the analyst
- C. AI assistance was used in parts of this analysis
- D. The rate was drafted by an assistant and recomputed by hand

#### [day3#lab-3-4] Method, disclosure and the capstone question

Lab 3.4 · 25 min

Write the method and disclosure paragraph from the log, test it against the log, and choose the capstone question.

[D3_4_disclosure.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D3_4_disclosure.ipynb)

- [ ] List the assisted steps from the log (5 min)
- [ ] Write the method and disclosure paragraph (8 min)
- [ ] Test the paragraph against the log; write the note (5 min)
- [ ] Choose the capstone question and route its tables (7 min)
- [ ] ✱ Stretch: Rewrite the paragraph in Arabic for an Arabic report

#### [day3#wrap-up] Leave behind what a colleague needs to stand where you stood

*Day 3 recap*

- **Route first:** a table takes its highest column; rows of Restricted tables never go to a hosted assistant; a guard enforces it.
- **Log as you go:** request, context, model, settings, code, data fingerprint, headline, check.

- **Reproduced** means a peer reaches the README's numbers from the package alone: matched, drifted or no step.
- **Disclose** the tool, the steps, the data seen, the verification and who signs, and say what was not verified.

> **Delegate, verify, reproduce.** The assistant drafts. You decide what it may do, prove what it did, and own what you sign.

#### [day3#next] Two hours to build the package, eight minutes to defend it

*Tomorrow · Capstone*

Start from labs/capstone. Brief, delegate, verify, repeat five times, log, disclose. A peer reruns your package. In the defence you recompute one headline number, chosen by the assessor, without the assistant.
