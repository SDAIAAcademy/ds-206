---
course: "Analysis with AI Assistants: Delegate, Verify, Reproduce"
code: "DS-206"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-206/slides/day1.html"
---

# Analysis with AI Assistants: Delegate, Verify, Reproduce

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
