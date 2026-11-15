# Package: (your question, in one line)

Analyst: (your name). Rerun by: (your peer's name, after the rerun).

## The question

(The question as you answer it: the population, the period, the one rate and its denominator.)

## Headline numbers

Written by `capstone/package.py readme` from `headline.json`. Do not type numbers here.

<!-- headline -->
<!-- /headline -->

## Findings

(Three to five sentences. Every number in them is in the table above. Say which conclusion held in all five runs.)

## Method and disclosure

(One paragraph, 60 to 150 words: the tool and model, the steps it drafted, the data it saw, how each step was verified and which was not, and who is accountable. Lab 3.4.)

## Files

- `brief.md`: the delegation plan and the brief with its acceptance checks.
- `AGENTS.md`: the project context file in force for every request.
- `run_log.jsonl`: one line per assisted step.
- `transcripts/`: the conversations as they happened, including rejected replies.
- `headline.json`: each headline number with the logged step and key it comes from.
- `notes.md`: one verification note per headline number.
- `variability.md`: five runs of one request.
- `data_handling.md`: each table's level and destination.
- `rerun_log.md`: written by the peer.

## How to rerun

From `labs/`: `uv run python capstone/package.py rerun <this folder>`.

All data is synthetic and describes nobody.
