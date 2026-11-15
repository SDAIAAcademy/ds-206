---
course: "Analysis with AI Assistants: Delegate, Verify, Reproduce"
code: "DS-206"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-206/"
---

# Analysis with AI Assistants: Delegate, Verify, Reproduce

Delegate analysis steps to an assistant, prove every number another way, and hand over work a peer can rerun

Participants analyse data with a coding assistant or agent in a notebook and stay accountable for every number. For a fictional courier company they decide which steps to delegate, brief the assistant with acceptance checks, prove results by recomputing key numbers another way, measure how answers vary between runs, decide which data may go to which assistant, and package an analysis that a peer reruns from logged prompts, code and data.

- **Audience:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.
- **Prerequisites:** FN-101 Python for Data and AI Work; FN-104 SQL and Data Wrangling; FN-106 Responsible Data and AI Practice in the Kingdom; Writes SQL joins and dataframe group-bys without assistance; Has completed one analysis end to end, from raw table to chart; Setup: a laptop with uv, or Google Colab. A key for a free hosted model (OpenRouter by default) is optional: every lab also runs on recorded replies. Nothing downloads a model. Run 00_setup_check before Day 1; see labs/README.md.
- **Case study:** Hudhud Parcel: Hudhud Parcel is a fictional courier in Riyadh, Jeddah, Dammam and Madinah whose operations director asks why late deliveries jumped in April and which city to fix first. Participants answer with Rafiq, a coding assistant in the notebook, on 500,000 synthetic deliveries over a year with attempt scans, driver shifts, route plans and 20,000 complaint texts in Arabic and English. The data is generated with a fixed seed and carries planted traps: a changed on-time definition, duplicated scans, UTC scan times, test shipments, plan versions that fan out a join, and a complaint export sorted so that a sample misstates one city and one language.

## Outcomes

- LO1 (Awareness): Identify which analysis steps suit delegation and which need the analyst's own judgement, with a reason for each, given a ten-step plan for the courier's late-delivery question
- LO2 (Applied): Prepare a delegation brief stating question, data, definitions, constraints and acceptance checks before the assistant runs, given the operations director's request and the delivery tables
- LO3 (Applied): Test assisted analyses by recomputing headline numbers another way and checking joins, filters, denominators and chart encodings, given three assisted analyses with seeded errors
- LO4 (Applied): Measure run-to-run variability by repeating one request five times and comparing code, numbers and conclusions, given a fixed prompt, dataset and model settings
- LO5 (Applied): Classify analysis data by sensitivity and assign each table to a local assistant, a hosted assistant or neither, given the courier tables and the organisation's assistant policy
- LO6 (Performance): Deliver an assisted analysis package that another analyst can rerun and audit from logged prompts, code, data and verification notes, given a new question and a two-hour budget

## Day 1: Delegate with intent

What an assistant decides for you when you do not, which steps to hand over, and how to brief them

#### [day1#title] Delegate with intent

*SDAIA Academy · Analysis with AI Assistants: Delegate, Verify, Reproduce*

Day 1: What an assistant decides for you when you do not, which steps to hand over, and how to brief them

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-206

#### [day1#agenda] Delegate with intent

*Today*

- **Session 1 · What assistants get wrong in analysis**: Assisted analysis fails quietly: the code runs, and the choices nobody stated decide the number
- **Session 2 · Delegate, assist or keep**: Three questions sort the steps of a plan: is it cheap to check, is judgement the product, are the stakes high
- **Session 3 · The delegation brief**: A brief states the question, the data, the definitions, the constraints and the checks before the assistant runs
- **Session 4 · Context files for a project**: A context file carries what holds for every request in a project; it lowers the number of errors and finds none

### Session 1: What assistants get wrong in analysis

#### [day1#s1] What assistants get wrong in analysis

*Session 1*

- Name the five places where an assisted analysis goes wrong without an error
- List the assumptions in an assistant's code, line by line
- Test an assumption by changing it and reading how far the number moves

#### [day1#it-ran-is-all-you-know] The code ran. That is all you know

*The case*

**Dareen, analyst:** What is our on-time delivery rate?

**Rafiq, assistant (weak example):** Your on-time delivery rate is 85.3%. I joined deliveries to their delivery scans and averaged the on-time flag.

**79.4%** the rate under Hudhud's own written definition

- **No error was raised.** Valid SQL, a number between 0 and 1, a confident sentence. Six points from the answer.

#### [day1#five-quiet-places] An analysis goes wrong quietly in five places

*Where to look*

| Place | The silent choice | At Hudhud |
| --- | --- | --- |
| **Definition** | What the measure means | The on-time rule changed on 1 April 2026; the system flag follows whichever was in force |
| **Grain** | What one row is, after each join | A scan can be uploaded twice; a route has several plan versions |
| **Filter** | Which rows left, and why | Test shipments, cancelled orders, the last day of a period |
| **Denominator** | Out of what | Delivered parcels, or every parcel that left a hub? |
| **Time** | Which clock, which calendar | Scan times are UTC, promises are local: three hours apart |

#### [day1#one-question-six-numbers] One question, six numbers, 9.7 points apart

*Lab 1.1, measured*

| Item | Value |
| --- | --- |
| D-1 all year, delivered only | 89.2% |
| The reply: flag, joined to scans | 85.3% |
| Flag, one row per parcel | 83.9% |
| Flag, tests removed | 83.8% |
| D-2 all year, delivered only | 81.9% |
| D-2 all year, dispatched | 79.4% |

> **Every row runs.** Each is "the on-time rate" under some reading. Only the last follows the written definition.

#### [day1#april-jump-is-the-ruler] The April jump is a change of ruler, not of deliveries

*The director's question, first look*

| On-time rate | March 2026 | April 2026 |
| --- | --- | --- |
| Dashboard tile (system flag) | 89.4% | 80.0% |
| D-2 applied to both months | 79.9% | 79.8% |

- **What changed on 1 April.** On time now means by the promised hour, and a parcel never delivered counts as late.
- **What an assistant sees.** A column named `on_time_flag`. Nothing in its name says it holds two rules.

#### [day1#agents-on-analysis-benchmarks] Agents are weakest where analysis needs several steps and context

*Beyond one case*

**14.55%** accuracy of the best agent on the hardest tasks of DABstep, over 450 multi-step data analysis tasks from a financial analytics platform

- **BLADE, 12 research datasets.** Compared with expert analysts, language models were "often limited to basic analyses".
- **What the hard tasks share.** Several steps, documentation that must be read, and one precise answer.

#### [day1#read-the-code-as-choices] Read the reply as a list of choices, not as an answer

*The method of Lab 1.1*

1. **1 · The measure** Which column or expression is averaged or counted?
2. **2 · Each join** What is one row before it, and after it?
3. **3 · Each filter** Which rows left? Which should have left and stayed?
4. **4 · The pool** Which periods and groups are folded into one number?

> **Then test.** Change one choice, rerun, read how far the number moves. A choice that moves it is an assumption worth stating.

#### [day1#check-it-ran] What do you know when the reply runs?

*Checkpoint*

**Question:** Rafiq returns a query for "share of parcels with a second delivery attempt". It runs without error and prints 0.11. What has been established?

- A. That 11% is about right, since the value is plausible
- B. That the query is valid SQL on these tables
- C. That the denominator is dispatched parcels
- D. That a second run would print 0.11 again

#### [day1#lab-1-1] One line in, six assumptions out

Lab 1.1 · 25 min

Give an assistant a one-line request; list every assumption it made, then test three of them with one query each.

[D1_1_one_line_request.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D1_1_one_line_request.ipynb)

- [ ] Send the one-line request and run the reply (5 min)
- [ ] List every assumption in the reply's code (8 min)
- [ ] Test three assumptions with one query each (8 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Send the same line to your own assistant and compare its assumptions

### Session 2: Delegate, assist or keep

#### [day1#s2] Delegate, assist or keep

*Session 2*

- Distinguish delegating a step, being assisted on it and keeping it
- Sort the steps of an analysis plan with a reason for each
- Explain what unchecked delegation costs the analyst's own skill

#### [day1#three-modes] Every step of a plan is delegated, assisted or kept

*A vocabulary*

- **Delegate.** The assistant does the step. You check the result with a light check: a count, the axes, a diff. **Profile the tables.**
- **Assist.** The assistant drafts. You do the part that decides the number, or you recompute it another way. **The monthly on-time rate.**
- **Keep.** You do it. The assistant may criticise your draft; it does not decide. **What "late" means this year.**

#### [day1#three-questions-sort] Three questions sort most steps

*A rule of thumb*

1. **Is judgement the product?** A definition, a causal claim, a recommendation. Then keep.
2. **Is the result cheap to check?** A count against the source, a chart you can read.
3. **Are the stakes high?** Would a wrong result reach a decision before anyone noticed?

```python
# file: Lab 1.2 · suggest
def suggest(step):
    if step["judgement_is_the_product"]:
        return "keep"
    if step["cheap_to_check"] and not step["high_stakes"]:
        return "delegate"
    return "assist"
```

> **The rule moves the judgement, it does not remove it.** Someone still decides what is cheap to check and what is high stakes.

#### [day1#ten-steps-sorted] Ten steps: three delegated, four assisted, three kept

*The late-delivery plan*

| # | Step | Mode | # | Step | Mode |
| --- | --- | --- | --- | --- | --- |
| 1 | Decide what late means | keep | 6 | Join route plans, long against short | assist |
| 2 | Load and profile the tables | delegate | 7 | Cause or coincidence in Dammam | keep |
| 3 | Remove tests and duplicate scans | assist | 8 | Summarise complaint categories | assist |
| 4 | Monthly on-time rate | assist | 9 | Tidy the notebook | delegate |
| 5 | Chart from the checked table | delegate | 10 | Recommend which city first | keep |

#### [day1#skill-formation-evidence] Learners who delegated everything finished, and learned less

*Why "keep" exists*

- **52** developers learning a new library, assigned at random to work with or without an assistant
- **17%** lower score for the assisted group on a quiz of understanding, code reading and debugging
- **3 of 6** ways of using the assistant kept learning intact: the ones with cognitive engagement

> **The skill that erodes is the one supervision needs.** Reading code and finding what is wrong with it is exactly the work of Day 2.

#### [day1#felt-faster-measured-slower] Feeling faster is not a measurement

*Your own sense of it*

| Item | Value |
| --- | --- |
| Forecast before the tasks | 24% faster |
| Belief after the tasks | 20% faster |
| Measured | 19% slower |

Sixteen experienced open-source developers, 246 tasks in their own projects, each task assigned at random to allow or forbid AI tools (early 2025).

#### [day1#confidence-and-checking] Confidence in the tool goes with less checking

*Who checks, and who does not*

- **Higher confidence in the assistant.** went with **less** critical thinking about its output.
- **Higher confidence in one's own skill.** went with **more** critical thinking about its output.

A survey of 319 knowledge workers who described 936 real uses of generative AI at work.

> **The habit this course builds.** The check is decided before the run, in the brief, so it does not depend on how confident you feel afterwards.

#### [day1#keep-is-not-a-ban] On a kept step the assistant argues; you decide

*Using the assistant on a kept step*

**You:** I will apply D-2 to the whole year. Give me the three strongest objections a board member could raise.

**Assistant (good example):** 1. The dashboard showed D-1 numbers for six months. 2. Staff were measured on D-1 then. 3. D-2 needs the promised hour, which older exports may lack.

- **Ask for objections**, missing cases, a second reading.
- **Do not ask** "which definition should I use?"
- The decision and its reason are written by you, in your words.
- If you cannot defend it without the assistant, it was not kept.

#### [day1#check-which-to-keep] Which step does the analyst keep?

*Checkpoint*

**Question:** Fawaz Al-Habib of customer care asks whether express parcels get more complaints. Four steps follow. Which one is kept?

- A. Counting complaints and parcels per service
- B. Drawing a bar chart of the two rates
- C. Drafting the query for complaints per 1,000 parcels
- D. Deciding whether complaints are counted per parcel or per customer

#### [day1#lab-1-2] Delegate, assist or keep

Lab 1.2 · 25 min

Sort a ten-step plan into delegate, assist or keep, with reasons, and score the marks against the reference.

[D1_2_delegate_assist_keep.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D1_2_delegate_assist_keep.ipynb)

- [ ] Read the plan and the three questions (5 min)
- [ ] Mark the ten steps, with a reason each (9 min)
- [ ] Write the rule as a function and compare (7 min)
- [ ] Write the note: the check for each delegated step (4 min)
- [ ] ✱ Stretch: Sort the steps of an analysis you did last month

### Session 3: The delegation brief

#### [day1#s3] The delegation brief

*Session 3*

- Write the five parts of a delegation brief
- Write acceptance checks that a reviewer can apply without asking the author
- Turn a failed check into a precise follow-up request

#### [day1#brief-five-parts] A brief has five parts, written before the assistant runs

*The delegation brief*

Prompt for Notebook assistant:

```text
For Tahani Al-Qasim: the monthly on-time rate, October 2025 to September 2026, as a table and one chart.
Use deliveries (one row per parcel) and customers. Month is the month of created_at. Do not join scans.
On time is D-2 for every month: delivered_at at or before promised_by; a dispatched parcel never delivered is late.
One query per step. No test shipments, no cancelled orders. Stop after each step and show its row count.
Twelve rows, 2025-10 to 2026-09. Deliveries sum to the dispatched, non-test parcels. No month moves more than 5 points.
```

Question · Data · Definitions · Constraints · Acceptance checks

#### [day1#check-or-wish] An acceptance check names a number, a count or a condition

*The fifth part*

| A wish | A check a reviewer can apply |
| --- | --- |
| The numbers should look reasonable | Every rate is between 0 and 1; no month differs from the one before by more than 5 points |
| Make sure nothing is double counted | The working table has one row per `delivery_id` |
| Cover the whole year | Exactly 12 rows, 2025-10 to 2026-09 |
| Use the right parcels | Deliveries sum to the dispatched, non-test parcels, counted by me |

> **The test of a check.** Could a colleague apply it to the output without asking you a question?

#### [day1#expected-comes-from-you] The expected value comes from your query, never from the reply

*Independence*

```python
# file: Lab 1.3 · check_total
def check_total(result):
    expected = U.one(con, """
        SELECT COUNT(*)
        FROM deliveries d
        JOIN customers c
          ON c.customer_id = d.customer_id
        WHERE c.segment <> 'TEST'
          AND d.status <> 'cancelled'""")
    got = int(result["deliveries"].sum())
    return got == expected, (got, expected)
```

- **A check that cannot fail.** "Ask the assistant to confirm its total" compares the answer with itself.
- **Small, and yours.** Five lines of SQL you wrote and understand are worth more than fifty you read.

#### [day1#small-steps-with-checkpoints] Small steps with a stop after each find errors while they are small

*Constraints that pay*

1. **Step 1 · Working table** stop: rows, tests removed, cancelled removed
2. **Step 2 · Monthly rate** stop: 12 rows, the total, the range
3. **Step 3 · Chart** stop: axis from zero, rates not counts

- **Stepwise.** An error is found one step after it is made, with one query to read.
- **All at once.** An agent that runs ten steps hands you ten steps of code and one number.

#### [day1#first-reply-fails-one-check] The first reply said the right words and failed one check

*Lab 1.3, measured*

| Check | First reply | After one follow-up |
| --- | --- | --- |
| Total equals dispatched parcels | *496,046 against 486,078* | 486,078 |
| Twelve months | pass | pass |
| Rates in range, no 5-point jump | pass | pass |
| Yearly on-time rate | 77.8% | 79.4% |

> **Its sentence was correct.** "Under D-2, without test shipments." The 9,968 cancelled orders in the denominator were visible only to the check.

#### [day1#follow-up-names-the-check] A follow-up names the check, the number it saw and the rule

*When a check fails*

**Vague:** This looks too low. Are you sure? Please double-check everything.

**Assistant (weak example):** You are right to question it. I have reviewed the query and it is correct. The rate is 77.8%.

**Precise:** Check 1 failed: the deliveries add up to more than the dispatched parcels. Cancelled orders are in no rate. Fix step 2.

**Assistant (good example):** I had left cancelled orders in the denominator. They are removed; the total equals the dispatched parcels.

#### [day1#check-acceptance] Which line is an acceptance check?

*Checkpoint*

**Question:** A brief asks for late deliveries per city for the year. Which line can Yasser apply to the result without asking the author anything?

- A. Four rows, one per city, and the late counts sum to my own count of late dispatched parcels
- B. Be careful not to double count parcels with several scans
- C. Use one query per step and stop after each step
- D. Have the assistant confirm that its totals are correct

#### [day1#lab-1-3] A brief with acceptance checks

Lab 1.3 · 25 min

Write a brief with acceptance checks for three steps and run it: one check fails, one follow-up fixes it.

[D1_3_delegation_brief.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D1_3_delegation_brief.ipynb)

- [ ] Complete the brief until it has no gaps (8 min)
- [ ] Write three acceptance checks as functions (8 min)
- [ ] Run the brief, apply the checks, follow up once (5 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Add a check that would have caught the flag's two definitions

### Session 4: Context files for a project

#### [day1#s4] Context files for a project

*Session 4*

- Decide what belongs in a project context file and what belongs in a brief
- Write the definitions, checks and prohibitions of an analysis project as rules
- Compare two runs of one brief on code, numbers and checks

#### [day1#context-file-is-a-readme-for-agents] A context file tells every request what the project already knows

*Project context*

- A plain text file in the project that the assistant reads **before every request**.
- One open convention is `AGENTS.md`: "a README for agents".
- Written for software projects: build steps, tests, code style.
- An analysis project needs different sections.

| Section | For an analysis project |
| --- | --- |
| Data | Tables, what one row is, what the assistant may see |
| Definitions | Measures, denominators, exclusions, time |
| Conventions | Engine, style, what a result looks like |
| Checks | What to run and show before answering |
| Do not | Joins and outputs that are never right here |

#### [day1#file-or-brief] The file holds what is true for every request; the brief holds this one

*What goes where*

- **In the context file.**
  - On time is D-2 for every month
  - Cancelled orders and test shipments are in no rate
  - Scan times are UTC
  - Never join scans to count parcels
- **In the brief.**
  - Tahani's question and her deadline
  - The steps of this task
  - The acceptance checks of this result
  - What to stop and show

> **Neither holds rows or secrets.** A context file is sent with every request, to whatever model is configured.

#### [day1#rules-not-essays] Write rules a reply can be held to, not explanations

*How to write it*

```markdown
<!-- file: AGENTS.md · Lab 1.4 -->
## Definitions
- On time is D-2 for every month:
  delivered_at <= promised_by.
- A dispatched parcel never delivered is late.
- Never use on_time_flag across months.
- Denominator: dispatched parcels
  (delivered, failed or returned).
- A parcel belongs to the month of created_at.

## Do not
- Do not join scans to count parcels.
```

- One fact per line, in the words of the columns.
- Each line can be checked against a reply.
- Short: long files are followed less well and cost tokens on every request.
- It has an owner and a date, like any definition.

#### [day1#same-brief-two-runs] One short brief, with and without the file

*Lab 1.4, measured*

| "Monthly on-time rate for Tahani, whole year." | Yearly rate | Off by | Checks passed |
| --- | --- | --- | --- |
| Without the context file | 86.7% | 7.3 points | 2 of 3 |
| With the context file | 81.9% | 2.5 points | 2 of 3 |
| Written definition, recomputed | 79.4% | 0 | 3 of 3 |

- **Without.** UTC scan times against local promises, test shipments kept, a join to scans.
- **With.** All of that fixed. One rule of the file ignored: delivered parcels only.

#### [day1#context-is-not-verification] A context file lowers the number of errors. It finds none

*The limit*

- **What it did.** Three of four errors did not happen. That is real, and cheap.
- **What it cannot do.** Tell you whether a given reply followed it. The file stated the denominator rule; the reply broke it.

> **Close the loop.** Every error that verification finds becomes a line in the file, or a check in the brief, or both. The file is the project's memory of its own mistakes.

#### [day1#check-context-file] What does the context file change?

*Checkpoint*

**Question:** Your project's context file states the on-time definition and the denominator. A reply arrives that says it followed both. What do you do with the reply's number?

- A. Report it, since the file was in place and the reply cites it
- B. Add a stricter line to the file, then report the number
- C. Apply the acceptance checks to it, exactly as without the file
- D. Discard it and write the query yourself from the start

#### [day1#lab-1-4] A project context file

Lab 1.4 · 25 min

Add a project context file, rerun a brief and compare the outputs on code, numbers and acceptance checks.

[D1_4_context_file.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D1_4_context_file.ipynb)

- [ ] Read the starting context file and find its gaps (4 min)
- [ ] Write the three missing sections (8 min)
- [ ] Rerun the brief without and with the file; compare (9 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Add the check the remaining error would fail by name

#### [day1#wrap-up] Decide before the run what you hand over and how you will know

*Day 1 recap*

- **Read for choices.** A reply that runs has proved its syntax. The measure, the grain, the filters and the denominator are choices to list and test.
- **Delegate, assist, keep.** Sort steps by whether you can check them cheaply, whether judgement is the product and what is at stake.
- **Brief and context.** State definitions and acceptance checks first. A context file lowers errors; only a check on the output finds them.

#### [day1#next] Verify: the errors that got through

*Tomorrow · Day 2*

Recompute a headline rate in SQL without the assistant and reconcile the gap, find four seeded errors in an assisted analysis, check a chart and a complaint summary against the data, and run one request five times.

## Day 2: Verify

Recompute the headline another way, count rows around every join, read charts and summaries against the data, and ask twice

#### [day2#title] Verify

*SDAIA Academy · Analysis with AI Assistants: Delegate, Verify, Reproduce*

Day 2: Recompute the headline another way, count rows around every join, read charts and summaries against the data, and ask twice

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-206

#### [day2#agenda] Verify

*Today*

- **Session 1 · Recompute it another way**: A number is verified when a second, independent path reaches it, and every point of the gap has a named cause
- **Session 2 · Joins, filters and denominators**: Most wrong numbers in assisted SQL come from rows that were multiplied, rows that were dropped, and a denominator nobody stated
- **Session 3 · Charts and words**: A chart is a set of encodings and a summary is a list of claims: each one is checked against a query
- **Session 4 · Ask it twice**: The same request gives different code and different numbers on different runs: only conclusions that hold in every run are reported as found

#### [day2#check-day1-review] What was missing from the one-line request?

*Review · Day 1*

**Question:** "What is our on-time delivery rate?" returned 85.3%; the written definition gives 79.4%. Which part of a brief would have prevented most of the gap?

- A. A longer statement of the question
- B. Constraints on the engine and the number of queries
- C. A more capable model
- D. The definitions: which on-time rule, and out of which parcels

### Session 1: Recompute it another way

#### [day2#s1] Recompute it another way

*Session 1*

- Choose a recomputation path that shares as little as possible with the first
- Recompute a headline rate in SQL without an assistant
- Reconcile two numbers by applying one difference at a time

#### [day2#two-stories-one-city] Two analyses of one city tell two stories

*Dammam, by quarter*

| On-time rate, Dammam | 2025 Q4 | 2026 Q1 | 2026 Q2 | 2026 Q3 | The story |
| --- | --- | --- | --- | --- | --- |
| Rafiq, in pandas | 86.9% | 87.1% | 87.1% | 84.3% | "Steady, a dip of under three points" |
| You, in SQL from the definitions | 79.6% | 80.0% | 79.7% | 72.3% | A fall of 7.4 points |

> **Two numbers that differ are not yet a finding.** One of them is wrong, or both are. Until the gap is explained you do not know which.

#### [day2#what-makes-a-path-independent] A second path verifies only what it does not share with the first

*Recompute another way*

- **Independent.**
  - Starts from the written definitions
  - Starts from the base table, one row per parcel
  - Written by you, before reading the first path's code closely
- **Not independent.**
  - The same query, translated to another engine
  - The same joined table, aggregated differently
  - The assistant asked to "double-check" its own answer

> **Share the question and the data. Share nothing else.**

#### [day2#ways-to-recompute] Five ways to reach the same number differently

*Choosing the second path*

| Another… | How | Catches |
| --- | --- | --- |
| **Starting table** | From deliveries only, no scans | Fan-outs, dropped rows |
| **Grain** | Daily counts first, then sum to the quarter | Period boundaries, averaging of averages |
| **Engine** | SQL if the first was pandas, or the reverse | Type and time handling, silent NULL rules |
| **Source** | A total from finance or the operations system | Missing or duplicated data upstream |
| **Sample by hand** | Twenty parcels, judged against the definition by eye | A definition coded wrongly in both paths |

#### [day2#reconcile-one-cause-per-row] Reconcile the gap one cause per row, until nothing is left

*Lab 2.1, measured*

| Dammam, third quarter of 2026 | On-time rate | Change |
| --- | --- | --- |
| Rafiq's method | 84.28% |  |
| + compare in local time, not UTC | 74.73% | *−9.54* |
| + quarter of `created_at`, not of the scan | 74.78% | +0.04 |
| + every dispatched parcel, undelivered ones late | 72.46% | *−2.31* |
| + no test shipments | 72.26% | −0.21 |
| Your SQL | 72.26% | 0 left |

- Change **one** choice per row.
- The first row reproduces their number; the last equals yours.
- The changes add up to the whole gap: 12.0 points.
- A remainder means an error nobody has found yet, possibly yours.

#### [day2#the-error-hid-the-finding] One time-zone error hid the one thing the director needed

*Why it mattered here*

- **−7.4 points** Dammam's on-time rate from the second to the third quarter of 2026, under D-2
- **−2.8 points** the same change in the assisted analysis

- **The mechanism.** A UTC scan time compared with a local promise makes every parcel delivered up to three hours after the cut-off look on time.
- **The coincidence.** Dammam's new problem is evening deliveries, just after the cut-off: exactly the parcels the error hides.

#### [day2#first-recomputation-is-yours] The first recomputation is done without the assistant

*The course's AI policy*

- **Independence.** A second query from the same assistant shares its reading of the columns and its habits.
- **Skill.** Reading code and finding what is wrong with it is the skill that erodes when it is never exercised.
- **Accountability.** In the defence you recompute one headline number live, with no assistant. Practise here.

> **After the first recomputation** the assistant is welcome: to explain a gap you have measured, or to write the tedious rows of a bridge you designed.

#### [day2#check-independent] Which recomputation is independent?

*Checkpoint*

**Question:** An assistant reports 3.1 failed parcels per 100 dispatched in Jeddah, from a query that joins deliveries to scans. Which second path tells you most?

- A. Rewriting the same query in pandas and comparing
- B. Asking the assistant to review its query for mistakes
- C. Counting failed and dispatched parcels from deliveries alone, by status
- D. Running the same query for Riyadh and checking it is similar

#### [day2#lab-2-1] Recompute and reconcile

Lab 2.1 · 25 min

Recompute an assistant's on-time rate in SQL and reconcile the gap, one cause per row.

[D2_1_recompute_in_sql.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D2_1_recompute_in_sql.ipynb)

- [ ] Run the assisted analysis and read its number (4 min)
- [ ] Recompute the rate yourself in SQL, without an assistant (8 min)
- [ ] Reconcile the gap, one cause per row (9 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Recompute a third time in pandas from the parquet file

### Session 2: Joins, filters and denominators

#### [day2#s2] Joins, filters and denominators

*Session 2*

- Count rows before and after each join to find a fan-out
- Find the rows a filter dropped with an anti-join
- State the denominator of a rate in one sentence and test the code against it

#### [day2#reading-someone-elses-joins] You can write a safe join. Today you audit one you did not write

*What you already know*

- **From SQL and Data Wrangling (FN-104).**
  - Grain, keys and cardinality
  - Filters and NULL
  - Joins that do not double count
  - Testing queries
- **What changes with an assistant.**
  - The query arrives complete and fluent
  - You did not make its choices, so you do not remember them
  - It joins tables you would have left out
  - Its sentence describes the intent, not the code

#### [day2#count-rows-around-each-join] Count rows and distinct keys after every join

*Check 1 · Lab 2.2, measured*

| Stage of the assisted query | Rows | Distinct parcels | Reading |
| --- | --- | --- | --- |
| deliveries, with its filters | 21,158 | 21,158 | One row is one parcel |
| + join `route_plans` | 22,699 | 21,158 | *1,541 extra rows: plan versions* |
| + left join `driver_shifts` | 23,778 | 21,158 | *More rows: split shifts* |
| + `AND s.hours >= 8` | 21,620 | 20,164 | *994 parcels gone* |

> **The fastest check in analysis.** If rows and distinct keys differ, one parcel has become several rows, and every average after it is weighted wrongly.

#### [day2#pick-the-row-you-mean] Several rows per key, and the join took them all

*Two fan-outs, one cause*

```sql
-- file: The plan in force is the highest version
WITH plan AS (
  SELECT *
  FROM route_plans
  QUALIFY version = MAX(version) OVER (
    PARTITION BY hub_id, plan_date, route_id)
)
FROM scope s
JOIN plan p
  ON p.hub_id = s.hub_id
 AND p.plan_date = s.route_date
 AND p.route_id = s.route_id
```

- **route_plans.** One row per version. A route replanned at midday has two or three.
- **driver_shifts.** One row per shift. A driver on a split shift has two that day.
- **The question to ask of every join.** What is one row of the table on the right, and is the join key unique in it?

#### [day2#left-join-made-inner] A condition on the right table turns a left join into an inner join

*A filter in the wrong place*

```sql
-- file: From the assisted query
LEFT JOIN driver_shifts s
  ON s.driver_id = d.driver_id
 AND s.shift_date = d.route_date
WHERE d.city = 'Dammam'
  AND d.status = 'delivered'
  AND s.hours >= 8
```

- **What it did.** Removed every parcel whose driver had no single shift of eight hours: 994 parcels on split-shift days.
- **What nobody asked.** The reply said "kept full shifts". The request never mentioned shifts.

#### [day2#anti-join-finds-the-missing] An anti-join against the scope names every missing row

*Check 2 · Lab 2.2, measured*

```sql
-- file: Which parcels of the scope are not in the result?
WITH scope AS (...),   -- from the sentence
     j AS (SELECT DISTINCT delivery_id
           FROM (...))  -- their joined rows
SELECT reason, COUNT(*) AS parcels
FROM scope
LEFT JOIN j
  ON j.delivery_id = scope.delivery_id
WHERE j.delivery_id IS NULL
GROUP BY reason
```

| Missing from the assisted result | Parcels |
| --- | --- |
| Driver on a split shift | 994 |
| Never delivered: failed or returned | 688 |
| Created on the last day | 236 |
| Of 22,082 in scope | 1,918 |

#### [day2#say-the-denominator] Say the denominator as a sentence, then test the code against it

*Check 3*

- **The sentence.** Dispatched Dammam parcels created in the three months, each counted once, classified by the plan in force on its route and day.

| Words of the sentence | What the code must show |
| --- | --- |
| dispatched | delivered, failed and returned; not cancelled |
| created in the three months | from 1 July up to, not including, 1 October |
| each counted once | rows equal distinct parcels |
| the plan in force | the highest version only |

> **If you cannot say it in one sentence, the rate has no meaning yet.** The sentence also goes into the report, under the number.

#### [day2#conclusion-survived-numbers-did-not] The conclusion survived. The numbers did not

*After the repair*

| Dammam, July to September 2026 | Short routes | Long routes | Gap | Counted |
| --- | --- | --- | --- | --- |
| Assisted query, four errors | 81.4% | 70.3% | 11.1 points | 21,620 rows |
| Corrected | 79.0% | 68.1% | 11.0 points | 22,082 parcels |

- **What to say.** Parcels on routes above 60 planned stops are on time 11 points less often: 68.1% against 79.0%.
- **What not to say.** "The direction was right." A report quotes rates, and both were over two points too high.

#### [day2#check-fan-out] Which check finds it first?

*Checkpoint*

**Question:** An assisted query joins complaints to deliveries to scans and reports "complaints per late parcel". You suspect a fan-out. What do you run first?

- A. Rows against distinct complaint ids after each join
- B. The final total, compared with last month's report
- C. An anti-join of complaints against the result
- D. A careful read of the join conditions

#### [day2#lab-2-2] Four seeded errors

Lab 2.2 · 25 min

Find the seeded join and filter errors in an assisted analysis, and name the check that found each.

[D2_2_joins_filters.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D2_2_joins_filters.ipynb)

- [ ] Run the assisted analysis and read its claim (4 min)
- [ ] Count rows before and after each join (7 min)
- [ ] Find the rows each filter dropped (6 min)
- [ ] State the denominator and recompute (4 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Repair the query and confirm the corrected comparison

### Session 3: Charts and words

#### [day2#s3] Charts and words

*Session 3*

- Read a chart's axis, measure and time window against the table behind it
- Split a written summary into claims and test each with a query
- Check that a summary does not misstate one city or language group

#### [day2#a-chart-is-three-encodings] Three encodings decide what a chart says

*Reading a chart you did not draw*

- **The measure.** What is on the y axis: a count or a rate? Of what, out of what?
- **The axis.** Where does it start? Is the scale the same for every series?
- **The window.** Which periods are shown, and is each one complete?

> **Read the code, not the picture.** An assistant's chart comes with the table and the plot call that made it: the encodings are written there.

#### [day2#same-data-two-charts] Same parcels, same weeks, opposite message

*Lab 2.3, drawn from the lab's run*

Figure: The assistant's chart: counts, an axis from 300, two partial weeks.

Figure: Redrawn: rates, an axis from 0, complete weeks.

#### [day2#count-or-rate] By count Riyadh is the problem. By rate it is Dammam

*The measure*

| Complete weeks since July | Riyadh | Dammam |
| --- | --- | --- |
| Late parcels per week | 847 | 464 |
| Share of dispatched parcels late | 20.3% | 27.7% |

- Tahani asked **which city to fix first**.
- A count answers "where are most of the late parcels?"
- A rate answers "where is the service worst?"
- Both are legitimate. The chart must say which it shows, and the title must not claim the other.

#### [day2#a-summary-is-a-list-of-claims] A summary is a list of claims, and each claim has a query

*Words · Lab 2.3, measured*

| The assistant's sentence | Verdict | All 20,000 complaints say |
| --- | --- | --- |
| Damaged parcels are the most common complaint, about half | *fails* | Late is first at 36%; damaged is 23% |
| Most complaints are written in English | *fails* | 56% are in Arabic |
| Madinah has the fewest complaints, so it needs the least attention | *fails* | Fewest by count, most per 1,000 parcels: 60.3 |
| Late-delivery complaints from Dammam rose after June | holds | From 94 to 144 a month |
| Arabic and English complaints raise the same issues | *fails* | Late is 40% of Arabic complaints, 32% of English |

#### [day2#what-the-summary-was-written-from] The summary was written from the first 500 rows

*Read the code before the words*

```python
# file: From the assistant's reply
sample = con.sql("""
    SELECT city, language, category, text
    FROM complaints LIMIT 500
""").df()
```

The export is sorted by channel, email first.

| Item | Value |
| --- | --- |
| English, first 500 | 92% |
| English, all complaints | 44% |
| Damaged, first 500 | 51% |
| Damaged, all complaints | 23% |

> **A model cannot read 20,000 texts in one request, so something chose which ones it read.** Find out what.

#### [day2#who-the-summary-misstated] The sample left out a city and a language

*Responsible use*

- **Madinah.** Fewest complaints by count: 3,239. Most per 1,000 parcels: **60.3**, against 38 to 40 in the other three cities. The summary: "needs the least attention".
- **Customers who write in Arabic.** 56% of all complaints. Late delivery is 40% of what they raise, against 32% for English. The summary: "the same issues in the same proportions".

> **A check for every summary.** Break the claim down by city and by language before it leaves your notebook. A group missing from the sample is a group the summary speaks for without having heard.

#### [day2#check-claim] Which sentence needs a different query?

*Checkpoint*

**Question:** An assistant writes: "Refund complaints are rare in Jeddah (742 of 5,573), so cash on delivery works well there." What do you check?

- A. That 742 of 5,573 is the right count for Jeddah
- B. The count, and refund complaints per 1,000 cash-on-delivery parcels by city
- C. A further 500 complaint texts from Jeddah, read by the assistant
- D. The share of refunds among Jeddah's complaints against other cities

#### [day2#lab-2-3] A chart and a summary against the data

Lab 2.3 · 25 min

Check an assistant's chart and complaint summary against the data, claim by claim.

[D2_3_charts_and_words.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D2_3_charts_and_words.ipynb)

- [ ] Recompute the charted series and read its encodings (8 min)
- [ ] Redraw the chart from the checked table (4 min)
- [ ] Test each sentence of the complaint summary (9 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Compute complaints per 1,000 parcels by city and language

### Session 4: Ask it twice

#### [day2#s4] Ask it twice

*Session 4*

- Explain why one request yields different analyses between runs
- Tabulate the analytic choices, numbers and conclusions of repeated runs
- Separate the conclusions that held in every run from those that did not

#### [day2#one-request-five-answers] One request, one context file, the same settings, five answers

*Lab 2.4, measured*

| Run | What it measured | Worst city | Dammam since July | Cities "worse" | Code like run 1 |
| --- | --- | --- | --- | --- | --- |
| 1 | D-2, dispatched parcels | Dammam | 72.3% | 1 | 1.00 |
| 2 | D-2, delivered parcels | Dammam | 74.6% | 1 | 0.82 |
| 3 | Late parcels per month | *Riyadh* | 2,042 a month | *4* | 0.37 |
| 4 | The system flag | Dammam | 72.3% | *4* | 0.73 |
| 5 | D-2, against April to June only | Dammam | 72.3% | 1 | 0.73 |

> **If you had asked once,** you would hold one of these five and would not know which.

#### [day2#why-runs-differ] Runs differ because the model samples and the request leaves room

*Sources of variation*

- **Sampling.** Each word is drawn from a distribution. Temperature widens or narrows it; few hosted models promise identical output even at zero.
- **Room in the request.** "Worst" and "got worse" each allow several measures and baselines. The model picks one per run.
- **A moving service.** A hosted model can be updated behind the same name. Next month's run is another run.

> **You control the middle one.** A brief that fixes the measure and the baseline removes most of the spread in the table.

#### [day2#many-analysts-one-dataset] Twenty-nine teams, one data set, one question

*Not only models*

- **0.89 to 2.93** range of the estimated effect, as odds ratios, across the teams
- **20 and 9** teams that found a significant effect, and teams that did not
- **21** different combinations of covariates among 29 analyses

> **The difference with an assistant.** A human analyst makes one set of choices and can be asked why. The assistant makes a new set on every run, silently.

#### [day2#which-conclusions-held] Report as found only what held in every run

*The variability table*

| Item | Value |
| --- | --- |
| Dammam got worse | 5 of 5 |
| Dammam is the worst city since July | 4 of 5 |
| No other city got worse | 3 of 5 |

- **Held in every run.** Robust to the choices the assistant varies. Still to be verified once.
- **Held in some.** Depends on a choice. Find the choice before the conclusion goes anywhere.

#### [day2#disagreement-is-not-a-vote] Three of five is not "60% true"

*Reading the disagreement*

| Run | Why it departed | Under the definitions |
| --- | --- | --- |
| 3 | Counted late parcels per month | A growing company has more of everything |
| 4 | Averaged the system flag | Two definitions before and after April |

- A choice is right or wrong under the definitions. It is not outvoted.
- Both departing runs broke a rule the context file states.
- Variability told you **where to look**. The definitions told you who was right.
- Then verify the run you keep, as in Lab 2.1.

#### [day2#stable-is-not-verified] Five identical answers can be identically wrong

*The limit*

- **What repetition shows.** How much the answer depends on the model's own variation.
- **What it cannot show.** An error every run shares: a column all five misread, a rule none was told.

- **Record what was repeated.**
  - The request and the context file, word for word
  - The model's name and version
  - Temperature, and a seed where the service supports one
  - The number of runs, and all of them, not the best one

#### [day2#check-five-same] Five runs agree. What do you know?

*Checkpoint*

**Question:** You send one request five times with the same settings. All five replies report 31.2% of Madinah's complaints about late delivery. What has been established?

- A. That 31.2% is correct, since five independent runs agree
- B. That any later run of the request will also give 31.2%
- C. That the number does not depend on this model's run-to-run variation
- D. That the five replies used the same code

#### [day2#lab-2-4] Five runs of one request

Lab 2.4 · 25 min

Repeat one request five times; tabulate differences in code, numbers and conclusions.

[D2_4_ask_it_twice.ipynb](https://sdaiaacademy.github.io/ds-206/labs/D2_4_ask_it_twice.ipynb)

- [ ] Run five replies to one fixed request (5 min)
- [ ] Tabulate choices, code and numbers per run (8 min)
- [ ] Decide which conclusions held in every run (8 min)
- [ ] Write the verification note (4 min)
- [ ] ✱ Stretch: Run the request five times live at temperature 0 and compare

#### [day2#wrap-up] A number is yours when a second path reaches it and the gap is explained

*Day 2 recap*

- **Recompute** from the definitions and the base table, without the assistant, then **reconcile** one cause per row.
- **Count** rows and distinct keys after each join; **anti-join** the scope; **say** the denominator.

- **Charts:** the measure, the axis, the window. **Summaries:** one query per claim, by city and by language.
- **Ask five times:** report what held in every run, and trace what did not to a choice.

> **What Tahani can now be told.** The April jump was the definition. Dammam fell 7.4 points from July, on long routes. Whether the optimiser caused it is yours to judge.

#### [day2#next] Reproduce and disclose

*Tomorrow · Day 3*

Decide which tables may reach a hosted assistant, a local one or neither; log one assisted analysis so that it can be rerun; rerun a colleague's package from its log; write the method and disclosure paragraph; and choose your capstone question.

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

## Capstone: Capstone: the assisted analysis package and its defence

A new question, a two-hour budget, a package a peer reruns, and eight minutes to defend it without an assistant

#### [capstone#title] Capstone: the assisted analysis package and its defence

*SDAIA Academy · Analysis with AI Assistants: Delegate, Verify, Reproduce*

Capstone: A new question, a two-hour budget, a package a peer reruns, and eight minutes to defend it without an assistant

Data Science Track · 3 teaching days + capstone day · 8 min talk and demo · DS-206

#### [capstone#agenda] How the day runs

*Capstone*

- **Build the package**: two hours, with the assistant: brief, delegate, verify, five runs, log, disclose
- **Peer rerun**: thirty minutes on a colleague's package, from its log alone
- **Defences**: eight minutes each, without the assistant, one number recomputed live
- **Review and closing**: what the packages showed, the follow-up task

#### [capstone#the-package] One question, one package, in a public repository

*What you hand over*

- **Start from** `labs/capstone/starter` and your choice from Lab 3.4.
- **Route first:** fill `data_handling.md` before the first request.
- **Log as you go:** every assisted step, with its transcript.
- **Recompute** each headline number without the assistant, and write its note.
- **Five runs** of one request, compared.
- **README:** numbers written from `headline.json`, and the disclosure paragraph.

- **Never in the repository.** A key, or a row or example value of a Restricted table, in any file or transcript.
- **Before you hand it over.** Run `capstone/package.py check`. It lists what the package still lacks.

#### [capstone#rubric] The rubric

*How packages are scored*

| Item | Value |
| --- | --- |
| Brief and delegation choices | 15% |
| Verification notes | 30% |
| Variability and reproducibility | 25% |
| Data handling and disclosure | 15% |
| Findings | 15% |

> **Findings are 15 of 100.** A smaller question with every headline number recomputed scores above a larger one that nobody checked.

#### [capstone#build] Two hours

*Build the package*

Commit as you go: the history is part of the evidence. Stop analysing when forty minutes remain.

#### [capstone#final-prep] Peer rerun · 30 minutes

*Before the first defence*

Clone your colleague's repository. Run `capstone/package.py rerun`. Ask nothing. Commit the rerun log to their repository.

#### [capstone#format] 8 minutes for each defence, without the assistant

*Format*

- **1 · Choices · 2 minutes.** The question. What you delegated, what you kept, and where the data went.
- **2 · Evidence · 3 minutes.** What verification found, which conclusion held in five runs, what your peer's rerun said.
- **3 · One number, live · 3 minutes.** The assessor chooses a headline number. You recompute it in SQL and explain any difference.

> **Peer feedback.** After each defence, everyone writes one strength, one question and one suggestion.

#### [capstone#running-order] Who defends when

*Running order*

| # | Presenter | Question |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#now-presenting] Defence and live recomputation

*Now presenting*

#### [capstone#review] What the packages showed

*Trainer review*

- **Strongest patterns.** Checks that found something, and disclosures that said what was not verified.
- **Common gaps.** Numbers with no step, denominators left unstated, steps logged from memory.
- **One surprise.** A conclusion that did not hold in five runs, or a null result that did.

#### [capstone#what-next] Keep going

*After the course*

- **The follow-up task:** one assisted analysis at work or on open data, with a verification note for each headline number, sent to your trainer
- **Your package stays yours:** its layout is the template for the next analysis you sign
- **At work:** your organisation's own classification and assistant policy decide what may go where; the course's policy was written for a fictional company
- **Next in the Academy:** the other courses of the Data Science track at level 200, which lead to the DS Assistant badge

#### [capstone#thanks] Thank you

*SDAIA Academy*

Analysis with AI Assistants: Delegate, Verify, Reproduce
