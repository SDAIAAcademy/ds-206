<!-- academy:title -->
# Analysis with AI Assistants: Delegate, Verify, Reproduce

تحليل البيانات مع المساعدات الذكية: التفويض والتحقق وقابلية إعادة الإنتاج

Data Science Track · SDAIA Academy · DS-206 · Level 200

REPLACE: one line under the title: what participants can do after the course

Participants analyse data with a coding assistant or agent in a notebook and stay accountable for every number. For a fictional courier company they decide which steps to delegate, brief the assistant with acceptance checks, prove results by recomputing key numbers another way, measure how answers vary between runs, decide which data may go to which assistant, and package an analysis that a peer reruns from logged prompts, code and data.

**Format:** Intensive: 3 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-206/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Identify which analysis steps suit delegation and which need the analyst's own judgement, with a reason for each, given a ten-step plan for the courier's late-delivery question | Awareness | the plan marked delegate, assist or keep, at least eight of ten matching the reference |
| LO2 | Prepare a delegation brief stating question, data, definitions, constraints and acceptance checks before the assistant runs, given the operations director's request and the delivery tables | Applied | a brief whose checks a reviewer can apply without asking the author |
| LO3 | Test assisted analyses by recomputing headline numbers another way and checking joins, filters, denominators and chart encodings, given three assisted analyses with seeded errors | Applied | a verification note per analysis naming each error and the check that found it |
| LO4 | Measure run-to-run variability by repeating one request five times and comparing code, numbers and conclusions, given a fixed prompt, dataset and model settings | Applied | a variability table stating which conclusions held in every run |
| LO5 | Classify analysis data by sensitivity and assign each table to a local assistant, a hosted assistant or neither, given the courier tables and the organisation's assistant policy | Applied | a data-handling table consistent with the classification policy |
| LO6 | Deliver an assisted analysis package that another analyst can rerun and audit from logged prompts, code, data and verification notes, given a new question and a two-hour budget | Performance | a repository that a peer reruns to the same headline numbers, defended live |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Delegate with intent | What assistants get wrong in analysis; Delegate, assist or keep; The delegation brief; Context files for a project | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Verify | Recompute it another way; Joins, filters and denominators; Charts and words; Ask it twice | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Reproduce and disclose | Which data may go where; Logging assisted work; The peer rerun; Disclosing assistance | [`slides/day3.html`](slides/day3.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Give an assistant a one-line request; list every assumption it made | [`D1_1_give_assistant_one.ipynb`](labs/D1_1_give_assistant_one.ipynb) |
| 1.2 | Day 1 · Session 2 | Sort a ten-step plan into delegate, assist or keep, with reasons | [`D1_2_sort_ten_step.ipynb`](labs/D1_2_sort_ten_step.ipynb) |
| 1.3 | Day 1 · Session 3 | Write a brief with acceptance checks for three steps and run it | [`D1_3_write_brief_acceptance.ipynb`](labs/D1_3_write_brief_acceptance.ipynb) |
| 1.4 | Day 1 · Session 4 | Add a project context file, rerun a brief and compare outputs | [`D1_4_add_project_context.ipynb`](labs/D1_4_add_project_context.ipynb) |
| 2.1 | Day 2 · Session 1 | Recompute an assistant's on-time rate in SQL and reconcile the gap | [`D2_1_recompute_assistant_s.ipynb`](labs/D2_1_recompute_assistant_s.ipynb) |
| 2.2 | Day 2 · Session 2 | Find seeded join and filter errors in an assisted analysis | [`D2_2_find_seeded_join.ipynb`](labs/D2_2_find_seeded_join.ipynb) |
| 2.3 | Day 2 · Session 3 | Check an assistant's chart and complaint summary against the data | [`D2_3_check_assistant_s.ipynb`](labs/D2_3_check_assistant_s.ipynb) |
| 2.4 | Day 2 · Session 4 | Repeat one request five times; tabulate differences in code, numbers and conclusions | [`D2_4_repeat_one_request.ipynb`](labs/D2_4_repeat_one_request.ipynb) |
| 3.1 | Day 3 · Session 1 | Decide which tables a local or a hosted assistant may process | [`D3_1_decide_which_tables.ipynb`](labs/D3_1_decide_which_tables.ipynb) |
| 3.2 | Day 3 · Session 2 | Log prompts, model settings and outputs for one analysis | [`D3_2_log_prompts_model.ipynb`](labs/D3_2_log_prompts_model.ipynb) |
| 3.3 | Day 3 · Session 3 | Rerun a supplied package from its logs; check the numbers match | [`D3_3_rerun_supplied_package.ipynb`](labs/D3_3_rerun_supplied_package.ipynb) |
| 3.4 | Day 3 · Session 4 | Write the method and disclosure paragraph; choose the capstone question | [`D3_4_write_method_disclosure.ipynb`](labs/D3_4_write_method_disclosure.ipynb) |
<!-- /academy:labs -->

## Capstone

An assisted analysis package for a new question in a public repository with prompts, agent transcripts, code, verification notes and a README of headline numbers a peer reproduced; eight-minute defence

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-104 SQL and Data Wrangling
- FN-106 Responsible Data and AI Practice in the Kingdom
- Writes SQL joins and dataframe group-bys without assistance
- Has completed one analysis end to end, from raw table to chart

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Coding assistant or agent with notebook access:** OpenCode with an open-weight model, a notebook with a connected assistant, such as marimo, a commercial coding agent
- **Local model server:** llama.cpp, Ollama
- **Analysis environment and notebooks:** Python with uv and marimo or JupyterLab, R with Quarto
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas
- **Version control:** Git with a hosted service, Git with a self-hosted server
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- SDAIA Generative AI Guidelines: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
