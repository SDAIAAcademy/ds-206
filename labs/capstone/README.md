# Capstone: the assisted analysis package

You answer one new question about Hudhud Parcel with an assistant, in two hours, and hand over a package
that a peer reruns. Then you defend it for eight minutes without the assistant.

## What you submit

A link to a **public repository** that holds your package: the files of `starter/`, filled in. The
repository contains synthetic course data only, no keys, and no row of a Restricted table in any
transcript. Your peer's `rerun_log.md` is committed in it before your defence.

## The questions

`questions.json` lists six questions this course has not answered, with the tables each needs. Your
choice from Lab 3.4 is in `artifacts/capstone/choice.json`. Your own question is welcome when your
trainer has approved it: it must be answerable from the Hudhud tables in two hours and have one rate
with a clear denominator.

## Two hours

| Minutes | Step | From |
|---|---|---|
| 10 | Copy `starter/` to your repository. Write the plan and the brief in `brief.md`, and complete `AGENTS.md` | Labs 1.2 to 1.4 |
| 10 | Fill `data_handling.md` before the first request | Lab 3.1 |
| 45 | Delegate, run, check, repair. Log every assisted step as it runs. Save the transcripts | Labs 1.3, 2.1, 2.2, 3.2 |
| 20 | Recompute each headline number without the assistant. Write a note for each in `notes.md` | Labs 2.1 to 2.3 |
| 15 | Send one request five times; fill `variability.md` | Lab 2.4 |
| 10 | Fill `headline.json`, write the README table from it, write the disclosure paragraph | Labs 3.3, 3.4 |
| 10 | Run the check, commit, push, hand the link to your peer | |

Your peer then needs about thirty minutes for the rerun.

## Logging a step

In a notebook opened in `labs/`, after the setup cell of any lab:

```python
import json
from pathlib import Path

PKG = Path("../../my-package")          # your repository's folder
context = (PKG / "AGENTS.md").read_text(encoding="utf-8")

request = "Follow the brief. Compute the second-attempt rate by city for cash-on-delivery parcels ..."
reply = U.ask(request, context, temperature=0.2, tables=["deliveries", "customers"], c=con)
U.show(reply)                           # read it before you run it
out = U.run_reply(reply, con)           # runs the code here: out.result, out.headline, out.error

record = U.log_record("cod_second_attempts", reply, out, ["deliveries", "customers"], con,
                      verified_by="recomputed in SQL without the assistant; equal to four decimals")
with open(PKG / "run_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
```

The assistant's code must set `result` (a dataframe) and `headline` (a dictionary of the numbers you will
quote). If you work with another assistant or agent, build the reply yourself and log it the same way:
`U.Reply(text=..., code=..., request=..., context=context, model="the model's name", settings={...})`.
Write `verified_by` only after the check has passed. A step you did not verify is logged with an empty
`verified_by`, and your disclosure says so.

With no key set, `U.ask` returns nothing. Then the code is yours: write it, wrap it in a `U.Reply` with
`model="none: written by the analyst"`, and say so in the disclosure. The package is scored the same way.

## The three commands

Run from `labs/`:

```
uv run python capstone/package.py readme ../../my-package    # writes the README table from headline.json
uv run python capstone/package.py check  ../../my-package    # lists what the package still lacks
uv run python capstone/package.py rerun  ../../my-package    # the peer runs this, and commits rerun_log.md
```

An entry of `headline.json`:

```json
{"name": "Second-attempt rate, cash on delivery, Riyadh", "value": 0.1234, "step": "cod_second_attempts", "key": "riyadh_cod"}
```

`step` is the step's name in the log and `key` is the key of that step's `headline`. The value above
only shows the shape; it is not an answer.

## The defence: eight minutes, no assistant

- Five minutes: what you delegated and what you kept, what verification found, which conclusion held in
  five runs, where the data went.
- Three minutes: the assessor chooses one headline number. You recompute it live, in SQL, without the
  assistant, and explain any difference.

## How it is scored

| Criterion | Weight | Full marks look like |
|---|---|---|
| Brief and delegation choices | 15 | A plan with a reason per step; a brief whose checks a reviewer can apply without asking you |
| Verification notes | 30 | Every headline number recomputed another way; joins, filters and denominators checked; the errors found are named |
| Variability and reproducibility | 25 | Five logged runs compared; the peer reaches every headline number from the log |
| Data handling and disclosure | 15 | A handling table consistent with the policy; a paragraph the log supports, including what was not verified |
| Findings | 15 | A direct answer to the question with its limits; a verified null result scores in full |
