# Analysis with AI Assistants: Delegate, Verify, Reproduce: labs

Twelve labs of 25 minutes on one case: **Hudhud Parcel**, a fictional courier with hubs in Riyadh,
Jeddah, Dammam and Madinah. All data is synthetic, built on your machine from a fixed seed, and
describes nobody.

## Quick start

- **Google Colab:** open a notebook from the course page. Its first cell clones this repository and
  installs one package.
- **Locally, with uv:** from `labs/`, run `uv sync`, then `uv run jupyter lab`.
- Run `00_setup_check.ipynb` once before Day 1. The first run builds the tables (about 20 seconds,
  about 30 MB in `labs/artifacts/`, which is not committed).
- On Windows, clone to a short path, or run `git config --global core.longpaths true` first.

A laptop processor is enough. No lab downloads or runs a model on your machine.

## The assistant, and what "recorded" means

The assistant of the labs is called Rafiq. A request goes out with the **names of tables and columns
only**; the reply is code, and the notebook runs it on your machine. No row leaves the notebook.

- **With no key, every lab runs in full on recorded replies.** The recorded replies are scripted for
  this course: written to carry the choices and errors it teaches, and labelled `rafiq-recorded-1`.
  They are not captured from any product and say nothing about how a particular product behaves.
- **With a key,** the cells that call `U.ask` also send the request to a free hosted model, so you can
  compare a live reply with the recorded one. Set `OPENROUTER_API_KEY` in your environment. The checks
  of every lab run on the recorded replies either way, so a lab never fails because a live model
  answered differently.
- `HUDHUD_MODEL` chooses another model (the default is a free one that was listed when the course was
  written; free listings change). `HUDHUD_BASE_URL` points the helper at any service that speaks the
  same chat protocol. An organisation that serves a model on its own machines, for instance with
  llama.cpp or Ollama, sets the address of that server here: this is the "local assistant" of Day 3.

## The labs

| Lab | Notebook | AI policy | What you produce |
|---|---|---|---|
| 1.1 | `D1_1_one_line_request` | AI-full | The assumptions behind a one-line answer; six defensible rates for one request |
| 1.2 | `D1_2_delegate_assist_keep` | AI-off | A ten-step plan marked delegate, assist or keep, with reasons |
| 1.3 | `D1_3_delegation_brief` | AI-full | A brief with acceptance checks, applied to two replies |
| 1.4 | `D1_4_context_file` | AI-full | A project context file, and the difference it made |
| 2.1 | `D2_1_recompute_in_sql` | AI-off first | A headline number recomputed in SQL and reconciled term by term |
| 2.2 | `D2_2_joins_filters` | AI-off first | Four seeded errors found with row counts and an anti-join |
| 2.3 | `D2_3_charts_and_words` | AI-off first | A chart and a summary tested against counts |
| 2.4 | `D2_4_ask_it_twice` | AI-full | A variability table of five runs |
| 3.1 | `D3_1_which_data_where` | AI-off | A data-handling table and a guard |
| 3.2 | `D3_2_run_log` | AI-full | A run log record, proved by a rerun |
| 3.3 | `D3_3_peer_rerun` | AI-off | A peer's rerun log for a supplied package |
| 3.4 | `D3_4_disclosure` | AI-full | A method and disclosure paragraph; your capstone question |

Every lab starts from supplied reference state, so a lab you missed does not block the next one. Every
exercise raises `NotImplementedError` until it is done, and the cells after it fall back to the
reference result. Every lab ends with a verification note: what the assistant produced, how it was
checked, what was wrong. The reference versions are in `solutions/`, with `solutions/answer_key.md`.

## The data

| Table | Rows | One row is |
|---|---|---|
| `hubs` | 6 | a hub |
| `customers` | 3,005 | a merchant account (five are test accounts) |
| `drivers` | 900 | a driver |
| `driver_shifts` | 65,757 | one shift; a split shift is two rows on one day |
| `route_plans` | 67,678 | one version of one route's plan for one day |
| `deliveries` | 500,000 | one parcel, 1 October 2025 to 30 September 2026 |
| `scans` | 565,680 | one delivery-attempt scan, in UTC |
| `complaints` | 20,000 | one complaint, in Arabic or English |

The definitions are in `data/docs/definitions.md`, the request that starts the course in
`data/docs/request.md`, and the company's assistant policy in `data/docs/assistant_policy.md`. The
policy is written for the course; it is not a national text.

### What is planted in the data (for trainers)

1. The definition of on time changed on 1 April 2026; `on_time_flag` follows the definition in force.
2. Scans uploaded twice in Jeddah in March and April 2026 (8,271 duplicates).
3. Scan times are in UTC; every other time is local.
4. Test shipments (3,954) and cancelled orders (9,968) sit in `deliveries`.
5. Route plans have versions: a join without the latest version multiplies parcels.
6. Split shifts: two shift rows for one driver on one day.
7. One real effect: Dammam's on-time rate falls from July 2026, on routes of more than 60 planned stops.
8. Riyadh has the most late parcels and Dammam the highest late rate.
9. The complaints export is sorted by channel: its first 500 rows are not a sample.
10. About a third of the complaint texts carry a mobile number.

## Helpers

`hudhud.py` is the one helper module; its docstring lists the calls. `prepare_data.py` builds the
tables. The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py`
(`uv run python _tools/py2nb.py` from `labs/`), which also writes `solutions/`. Edit the sources, not
the notebooks. `_tools/make_recorded.py`, `rec_day2.py` and `rec_day3.py` write the recorded replies,
`_tools/make_package.py` builds the package that Lab 3.3 reruns, and `_tools/make_known_replies.py`
writes the known cases of Lab 3.1's screen and computes the screen example of the Day 3 slides.

Set `HUDHUD_QUICK=1` to shorten the cells that call a live model (two live runs in Lab 2.4, not five).

## Pre-work and capstone

- `prework/README.md`: two hours before Day 1, with the tutor instruction and the entry quiz.
- `capstone/README.md`: the capstone brief, the package starter and its three commands.
