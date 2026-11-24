---
course: "Analysis with AI Assistants: Delegate, Verify, Reproduce"
code: "DS-206"
version: "2027.2.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-206/index.html"
---

# Analysis with AI Assistants: Delegate, Verify, Reproduce

تحليل البيانات مع المساعدات الذكية: التفويض والتحقق وقابلية إعادة الإنتاج

Data Science Track · 3 teaching days + capstone day · 21 hours · Level 200

Delegate analysis steps to an assistant, prove every number another way, and hand over work a peer can rerun

Participants analyse data with a coding assistant or agent in a notebook and stay accountable for every number. For a fictional courier company they decide which steps to delegate, brief the assistant with acceptance checks, prove results by recomputing key numbers another way, measure how answers vary between runs, decide which data may go to which assistant, and package an analysis that a peer reruns from logged prompts, code and data.

**Who it is for:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.

**Format:** Intensive: 3 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Hudhud Parcel.** Hudhud Parcel is a fictional courier in Riyadh, Jeddah, Dammam and Madinah whose operations director asks why late deliveries jumped in April and which city to fix first. Participants answer with Rafiq, a coding assistant in the notebook, on 500,000 synthetic deliveries over a year with attempt scans, driver shifts, route plans and 20,000 complaint texts in Arabic and English. The data is generated with a fixed seed and carries planted traps: a changed on-time definition, duplicated scans, UTC scan times, test shipments, plan versions that fan out a join, and a complaint export sorted so that a sample misstates one city and one language.

## The course

### Day 1: Delegate with intent

Slides: https://sdaiaacademy.github.io/ds-206/slides/day1.md

- **Session 1: What assistants get wrong in analysis**
  - Name the five places where an assisted analysis goes wrong without an error
  - List the assumptions in an assistant's code, line by line
  - Test an assumption by changing it and reading how far the number moves
  - [Lab 1.1: One line in, six assumptions out (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D1_1_one_line_request.ipynb)
- **Session 2: Delegate, assist or keep**
  - Distinguish delegating a step, being assisted on it and keeping it
  - Sort the steps of an analysis plan with a reason for each
  - Explain what unchecked delegation costs the analyst's own skill
  - [Lab 1.2: Delegate, assist or keep (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D1_2_delegate_assist_keep.ipynb)
- **Session 3: The delegation brief**
  - Write the five parts of a delegation brief
  - Write acceptance checks that a reviewer can apply without asking the author
  - Turn a failed check into a precise follow-up request
  - [Lab 1.3: A brief with acceptance checks (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D1_3_delegation_brief.ipynb)
- **Session 4: Context files for a project**
  - Decide what belongs in a project context file and what belongs in a brief
  - Write the definitions, checks and prohibitions of an analysis project as rules
  - Compare two runs of one brief on code, numbers and checks
  - [Lab 1.4: A project context file (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D1_4_context_file.ipynb)

### Day 2: Verify

Slides: https://sdaiaacademy.github.io/ds-206/slides/day2.md

- **Session 1: Recompute it another way**
  - Choose a recomputation path that shares as little as possible with the first
  - Recompute a headline rate in SQL without an assistant
  - Reconcile two numbers by applying one difference at a time
  - [Lab 2.1: Recompute and reconcile (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D2_1_recompute_in_sql.ipynb)
- **Session 2: Joins, filters and denominators**
  - Count rows before and after each join to find a fan-out
  - Find the rows a filter dropped with an anti-join
  - State the denominator of a rate in one sentence and test the code against it
  - [Lab 2.2: Four seeded errors (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D2_2_joins_filters.ipynb)
- **Session 3: Charts and words**
  - Read a chart's axis, measure and time window against the table behind it
  - Split a written summary into claims and test each with a query
  - Check that a summary does not misstate one city or language group
  - [Lab 2.3: A chart and a summary against the data (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D2_3_charts_and_words.ipynb)
- **Session 4: Ask it twice**
  - Explain why one request yields different analyses between runs
  - Tabulate the analytic choices, numbers and conclusions of repeated runs
  - Separate the conclusions that held in every run from those that did not
  - [Lab 2.4: Five runs of one request (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D2_4_ask_it_twice.ipynb)

### Day 3: Reproduce and disclose

Slides: https://sdaiaacademy.github.io/ds-206/slides/day3.md

- **Session 1: Which data may go where**
  - Classify the tables of an analysis by their most sensitive column
  - Assign each table to a hosted assistant, a local assistant or neither under a written policy
  - Enforce the assignment with a guard that runs before any prompt leaves
  - [Lab 3.1: Hosted, local or neither (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D3_1_which_data_where.ipynb)
- **Session 2: Logging assisted work**
  - List what a log record must hold for a step to be rerun
  - Write a log record with a data fingerprint for one assisted step
  - Find what an incomplete log lacks before someone else has to
  - [Lab 3.2: A run log (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D3_2_run_log.ipynb)
- **Session 3: The peer rerun**
  - Rerun a package from its log without asking its author
  - Classify each headline number as matched, drifted or without a step
  - Write a rerun log that an assessor can read in two minutes
  - [Lab 3.3: Rerun a supplied package (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D3_3_peer_rerun.ipynb)
- **Session 4: Disclosing assistance**
  - Derive the assisted steps of an analysis from its log
  - Write a method and disclosure paragraph that the log supports
  - Choose a capstone question and route its tables before starting
  - [Lab 3.4: Method, disclosure and the capstone question (25 min)](https://sdaiaacademy.github.io/ds-206/labs/D3_4_disclosure.ipynb)

### Capstone: Capstone: the assisted analysis package and its defence

Slides: https://sdaiaacademy.github.io/ds-206/slides/capstone.md

## Capstone

An individual assisted analysis of a new question about Hudhud Parcel, built in two hours from the course starter (labs/capstone/): a delegation plan and brief, a project context file, the assistant's transcripts and a run log, the code, a verification note per headline number, a variability table of five runs, a data-handling table and a method and disclosure paragraph. A peer reruns the package from its log before the defence.

**What you submit:** A public repository whose README states the headline numbers a peer reproduced, with the prompts, agent transcripts, code, verification notes, run log and peer rerun log committed. Then an eight-minute defence without the assistant: five minutes on the delegation choices and what verification found, then the participant recomputes one headline number the assessor selects, live.

**Rubric:**

- Brief and delegation choices: 15%
- Verification notes: 30%
- Variability and reproducibility: 25%
- Data handling and disclosure: 15%
- Findings: 15%

## Outcomes

- **LO1** Identify which analysis steps suit delegation and which need the analyst's own judgement, with a reason for each, given a ten-step plan for the courier's late-delivery question (Awareness) Evidence: the plan marked delegate, assist or keep, at least eight of ten matching the reference
- **LO2** Prepare a delegation brief stating question, data, definitions, constraints and acceptance checks before the assistant runs, given the operations director's request and the delivery tables (Applied) Evidence: a brief whose checks a reviewer can apply without asking the author
- **LO3** Test assisted analyses by recomputing headline numbers another way and checking joins, filters, denominators and chart encodings, given three assisted analyses with seeded errors (Applied) Evidence: a verification note per analysis naming each error and the check that found it
- **LO4** Measure run-to-run variability by repeating one request five times and comparing code, numbers and conclusions, given a fixed prompt, dataset and model settings (Applied) Evidence: a variability table stating which conclusions held in every run
- **LO5** Classify analysis data by sensitivity and assign each table to a local assistant, a hosted assistant or neither, given the courier tables and the organisation's assistant policy (Applied) Evidence: a data-handling table consistent with the classification policy
- **LO6** Deliver an assisted analysis package that another analyst can rerun and audit from logged prompts, code, data and verification notes, given a new question and a two-hour budget (Performance) Evidence: a repository that a peer reruns to the same headline numbers, defended live

## Tools

- **Coding assistant or agent with notebook access:** OpenCode with an open-weight model, a notebook with a connected assistant, such as marimo, a commercial coding agent
- **Local model server:** llama.cpp, Ollama
- **Analysis environment and notebooks:** Python with uv and marimo or JupyterLab, R with Quarto
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas
- **Version control:** Git with a hosted service, Git with a self-hosted server

## Prerequisites

- FN-101 Python for Data and AI Work
- FN-104 SQL and Data Wrangling
- FN-106 Responsible Data and AI Practice in the Kingdom
- Writes SQL joins and dataframe group-bys without assistance
- Has completed one analysis end to end, from raw table to chart
- Setup: a laptop with uv, or Google Colab. A key for a free hosted model (OpenRouter by default) is optional: every lab also runs on recorded replies. Nothing downloads a model. Run 00_setup_check before Day 1; see labs/README.md.

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

---

SDAIA Academy · Data Science Track · Analysis with AI Assistants: Delegate, Verify, Reproduce

Course version 2027.2.0 · engine 1.0.0 · built 2026-11-24 · commit 8f871bb
