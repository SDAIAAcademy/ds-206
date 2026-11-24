---
course: "Analysis with AI Assistants: Delegate, Verify, Reproduce"
code: "DS-206"
version: "2027.2.0"
deck: "capstone"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-206/slides/capstone.html"
---

# Analysis with AI Assistants: Delegate, Verify, Reproduce

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
