"""Build the supplied package of Lab 3.3 and 3.4, data/packages/dammam_q3/, from the recorded replies.

    uv run python _tools/make_package.py

The log is written from real runs on the synthetic data, so its fingerprints and headline numbers are
the ones a participant's rerun produces. Two things are planted in the README on purpose:
one number that drifted from its logged step, and one number that no logged step produces.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS))
import hudhud as U  # noqa: E402

OUT = LABS / "data" / "packages" / "dammam_q3"
STEPS = [
    ("dammam_quarters", "assist", ["deliveries", "customers"], "recomputed in SQL from definitions.md without the assistant; reconciled to 0 points"),
    ("long_short", "assist", ["deliveries", "customers", "route_plans"], "row counts after each join and an anti-join against the scope; denominator stated"),
    ("weekly_chart", "delegate", ["deliveries", "customers"], ""),
]


def main() -> None:
    con = U.con()
    OUT.mkdir(parents=True, exist_ok=True)
    log = []
    for i, (name, mode, tables, verified) in enumerate(STEPS, 1):
        reply = U.recorded("3.3", name)
        out = U.run_reply(reply, con)
        assert not out.error, out.error
        rec = U.log_record(name, reply, out, tables, con, mode=mode, verified_by=verified)
        rec = {"seq": i, "date": "2026-10-12", **rec}
        log.append(rec)
    (OUT / "run_log.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in log), encoding="utf-8", newline="\n")
    h = {r["step"]: r["headline"] for r in log}
    numbers = [
        {"name": "Dammam on-time rate, third quarter of 2026", "value": h["dammam_quarters"]["q3_2026"], "step": "dammam_quarters", "key": "q3_2026"},
        {"name": "Dammam on-time rate, second quarter of 2026", "value": h["dammam_quarters"]["q2_2026"], "step": "dammam_quarters", "key": "q2_2026"},
        {"name": "On-time rate on long routes, Dammam, July to September", "value": 0.6841, "step": "long_short", "key": "long"},
        {"name": "Late-delivery complaints from Dammam per month since July", "value": 144, "step": None, "key": None},
    ]
    (OUT / "headline.json").write_text(json.dumps(numbers, indent=1) + "\n", encoding="utf-8", newline="\n")
    readme = f"""# Package: why Dammam is late since July

Analyst: Dareen Al-Sulaiman, Hudhud Parcel. Reviewed by: nobody yet. Rerun by: nobody yet.

## Headline numbers

| Number | Value |
|---|---|
| Dammam on-time rate, third quarter of 2026 | {h['dammam_quarters']['q3_2026']:.1%} |
| Dammam on-time rate, second quarter of 2026 | {h['dammam_quarters']['q2_2026']:.1%} |
| On-time rate on long routes, Dammam, July to September | 68.4% |
| Late-delivery complaints from Dammam per month since July | 144 |

## Files

- `run_log.jsonl`: one line per assisted step: request, model, settings, code, data fingerprints, headline, how it was verified.
- `headline.json`: the numbers above, each with the logged step and key it comes from.
- `notes.md`: the verification notes.

## How to rerun

Run each line of `run_log.jsonl` against the tables and compare with `headline.json`. Lab 3.3 does this.

All data is synthetic.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    notes = """# Verification notes

## dammam_quarters

**What the assistant produced.** Dammam by quarter under D-2: 79.7% in the second quarter of 2026, 72.3% in the third.
**How it was checked.** Recomputed in SQL from definitions.md without the assistant; reconciled to 0 points.
**What was wrong.** Nothing in this version. An earlier reply compared UTC scans with local promises (Lab 2.1).

## long_short

**What the assistant produced.** On-time rate on long routes against short ones, Dammam, July to September.
**How it was checked.** Row counts after each join, an anti-join against the scope, the denominator stated.
**What was wrong.** An earlier version joined every plan version; this version takes the plan in force.

## weekly_chart

**What the assistant produced.** A weekly late-rate chart for Riyadh and Dammam.
**How it was checked.** Not checked yet.
**What was wrong.** Unknown.
"""
    (OUT / "notes.md").write_text(notes, encoding="utf-8", newline="\n")
    print("package written:", [p.name for p in sorted(OUT.iterdir())], h)


if __name__ == "__main__":
    main()
