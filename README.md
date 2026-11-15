<!-- academy:title -->
# Analysis with AI Assistants: Delegate, Verify, Reproduce

تحليل البيانات مع المساعدات الذكية: التفويض والتحقق وقابلية إعادة الإنتاج

Data Science Track · SDAIA Academy · DS-206 · Level 200

Delegate analysis steps to an assistant, prove every number another way, and hand over work a peer can rerun

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
| Capstone | Capstone: the assisted analysis package and its defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Hudhud Parcel (هدهد للطرود).** A fictional courier with hubs in Riyadh, Jeddah, Dammam and Madinah. Its operations director asks one question, "why are we late?", and an analyst answers it over three days with an assistant called Rafiq: Day 1 turns the request into a brief, Day 2 proves the assistant's numbers, Day 3 packages the work so that a peer can rerun it.

The data is synthetic, built on the participant's machine from a fixed seed, and describes nobody: 500,000 deliveries over one year, with scans, route plans, driver shifts and 20,000 complaint texts in Arabic and English. Ten problems are planted in it, among them a definition of "on time" that changed in April, scans uploaded twice and one real effect in Dammam; `labs/README.md` lists them for trainers.

**The assistant in the labs.** A request carries table and column names only, the reply is code, and the notebook runs it locally. Every lab runs in full without a key, on recorded replies that were scripted for the course and are labelled as such; with a key for a free hosted model, the same cells also show a live reply. No lab downloads or runs a model on the participant's machine.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | One line in, six assumptions out | [`D1_1_one_line_request.ipynb`](labs/D1_1_one_line_request.ipynb) |
| 1.2 | Day 1 · Session 2 | Delegate, assist or keep | [`D1_2_delegate_assist_keep.ipynb`](labs/D1_2_delegate_assist_keep.ipynb) |
| 1.3 | Day 1 · Session 3 | A brief with acceptance checks | [`D1_3_delegation_brief.ipynb`](labs/D1_3_delegation_brief.ipynb) |
| 1.4 | Day 1 · Session 4 | A project context file | [`D1_4_context_file.ipynb`](labs/D1_4_context_file.ipynb) |
| 2.1 | Day 2 · Session 1 | Recompute and reconcile | [`D2_1_recompute_in_sql.ipynb`](labs/D2_1_recompute_in_sql.ipynb) |
| 2.2 | Day 2 · Session 2 | Four seeded errors | [`D2_2_joins_filters.ipynb`](labs/D2_2_joins_filters.ipynb) |
| 2.3 | Day 2 · Session 3 | A chart and a summary against the data | [`D2_3_charts_and_words.ipynb`](labs/D2_3_charts_and_words.ipynb) |
| 2.4 | Day 2 · Session 4 | Five runs of one request | [`D2_4_ask_it_twice.ipynb`](labs/D2_4_ask_it_twice.ipynb) |
| 3.1 | Day 3 · Session 1 | Hosted, local or neither | [`D3_1_which_data_where.ipynb`](labs/D3_1_which_data_where.ipynb) |
| 3.2 | Day 3 · Session 2 | A run log | [`D3_2_run_log.ipynb`](labs/D3_2_run_log.ipynb) |
| 3.3 | Day 3 · Session 3 | Rerun a supplied package | [`D3_3_peer_rerun.ipynb`](labs/D3_3_peer_rerun.ipynb) |
| 3.4 | Day 3 · Session 4 | Method, disclosure and the capstone question | [`D3_4_disclosure.ipynb`](labs/D3_4_disclosure.ipynb) |
<!-- /academy:labs -->

## Capstone

An assisted analysis package for a new question in a public repository with prompts, agent transcripts, code, verification notes and a README of headline numbers a peer reproduced; eight-minute defence

**Submission:** a link to a public repository built from `labs/capstone/starter`, holding the brief, the context file, the run log and transcripts, the code, the verification notes, the variability table, the data-handling table and a README whose headline numbers are written from the log. A peer's rerun log is committed in it before the defence. The repository holds synthetic course data only. The brief, the two-hour plan and the scoring guide are in `labs/capstone/README.md`.

**Defence:** eight minutes without the assistant: five on the delegation choices and what verification found, then one headline number, chosen by the assessor, recomputed live.

## Before and after the course

- **Pre-work (two hours):** the setup check, an entry quiz on joins and group-bys, and an hour with an assistant used as a tutor: `labs/prework/README.md`.
- **Follow-up task:** one assisted analysis at work or on open data, with a verification note for each headline number, sent to the trainer.
- **Practice questions:** `assessments/bank.json`, 32 questions across the six outcomes, published on the practice page of the course site.
- **The supervised check** (AI-off: find the errors in a printed assisted analysis and recompute two numbers in SQL) is an exam and is not in this repository.

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

### Evidence on assisted work and skill

- [Shen and Tamkin: How AI Impacts Skill Formation (2026)](https://arxiv.org/abs/2601.20245)
- [Becker et al. (METR): Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089)
- [Lee et al.: The Impact of Generative AI on Critical Thinking (Microsoft Research, CHI 2025)](https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/)

### Assistants and agents in data analysis

- [DABstep: Data Agent Benchmark for Multi-step Reasoning](https://arxiv.org/abs/2506.23719)
- [BLADE: Benchmarking Language Model Agents for Data-Driven Science](https://arxiv.org/abs/2408.09667)
- [Silberzahn et al.: Many Analysts, One Data Set (2018)](https://doi.org/10.1177/2515245917747646)

### Tools and conventions

- [AGENTS.md, the context-file convention](https://agents.md/)
- [marimo: in-editor AI assistance](https://docs.marimo.io/guides/editor_features/ai_completion/)
- [OpenCode documentation](https://opencode.ai/docs/)
- [DuckDB documentation](https://duckdb.org/docs/)
- [Ollama](https://ollama.com/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [OpenRouter: models](https://openrouter.ai/models)

### National references

- [Generative AI Guidelines for Government (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf)
- [Generative AI Guidelines for the Public (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenerativeAIPublicEN.pdf)
- [Data Classification Policy (NDMO, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [AI Ethics Principles (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
<!-- /academy:sources -->

### How the national references are used

- **Generative AI Guidelines for Government and for the Public (SDAIA):** the basis of Day 3: what may be entered into a generative AI tool, keeping a record of an assisted analysis, marking and verifying generated code, and disclosing assistance.
- **Data Classification Policy (NDMO):** the four levels behind the data-handling table of Lab 3.1. The assistant policy of Hudhud Parcel is fictional, written for the course on top of these levels, and says so.
- **Personal Data Protection Law and its Implementing Regulation:** why complaint texts, phone numbers and driver records are treated as personal data in the labs. The course does not teach the law; FN-106 does.
- **AI Ethics Principles (SDAIA):** accountability and transparency, which the course turns into two habits: the analyst signs every number, and every report says what an assistant did.
