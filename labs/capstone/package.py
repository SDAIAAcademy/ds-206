"""Three commands for an assisted analysis package (run from labs/):

    uv run python capstone/package.py readme <package>   # write the README's table of headline numbers from headline.json
    uv run python capstone/package.py check  <package>   # what the package still lacks
    uv run python capstone/package.py rerun  <package>   # the peer's command: rerun the log, trace every headline number

A package is a folder with README.md, run_log.jsonl and headline.json (see capstone/starter/).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hudhud as U  # noqa: E402

START, END = "<!-- headline -->", "<!-- /headline -->"
FILES = ["README.md", "brief.md", "AGENTS.md", "run_log.jsonl", "headline.json", "notes.md", "variability.md",
         "data_handling.md", "rerun_log.md"]


def read_log(pkg: Path) -> list[dict]:
    path = pkg / "run_log.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_claims(pkg: Path) -> list[dict]:
    path = pkg / "headline.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def fmt(value) -> str:
    if value is None:
        return ""
    return f"{value * 100 + 1e-9:.1f}%" if isinstance(value, float) and 0 <= value <= 1 else f"{value:,}"


def readme(pkg: Path) -> None:
    """Write the table between the two markers of README.md from headline.json."""
    claims = read_claims(pkg)
    steps = {r["step"] for r in read_log(pkg)}
    for c in claims:
        if c.get("step") not in steps:
            raise SystemExit(f"'{c['name']}' names the step {c.get('step')!r}, which is not in run_log.jsonl. Log the step first.")
    table = "\n".join(["| Number | Value | Logged step |", "|---|---|---|"] +
                      [f"| {c['name']} | {fmt(c['value'])} | `{c['step']}` |" for c in claims])
    path = pkg / "README.md"
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"README.md needs the two marker lines {START} and {END}")
    head, rest = text.split(START, 1)
    path.write_text(head + START + "\n" + table + "\n" + END + rest.split(END, 1)[1], encoding="utf-8")
    print(f"README.md: {len(claims)} headline numbers written from headline.json")


def disclosure(pkg: Path) -> str:
    text = (pkg / "README.md").read_text(encoding="utf-8") if (pkg / "README.md").exists() else ""
    m = re.search(r"^## Method and disclosure\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def check(pkg: Path) -> int:
    """List what the package still lacks. Returns the number of problems."""
    problems = [f"missing file: {f}" for f in FILES if not (pkg / f).exists()]
    log = read_log(pkg)
    if not log:
        problems.append("run_log.jsonl has no record")
    for rec in log:
        gaps = [g for g in U.log_gaps(rec) if g != "verified_by"]
        if gaps:
            problems.append(f"log step {rec.get('step')!r} lacks: {', '.join(gaps)}")
        if not rec.get("verified_by"):
            print(f"  note: step {rec.get('step')!r} has no verification recorded; the disclosure must say so")
    steps = {r.get("step") for r in log}
    claims = read_claims(pkg)
    if not claims:
        problems.append("headline.json has no number")
    problems += [f"headline number '{c['name']}' has no logged step" for c in claims if c.get("step") not in steps]
    para = disclosure(pkg)
    if not para:
        problems.append("README.md has no section '## Method and disclosure'")
    elif log:
        problems += [f"disclosure: {p}" for p in U.disclosure_check(para, log)]
    transcripts = [p for p in (pkg / "transcripts").glob("*") if p.name != "README.md"] if (pkg / "transcripts").exists() else []
    if not transcripts:
        problems.append("transcripts/ holds no transcript")
    for p in problems:
        print(" ✗", p)
    print(f"{len(problems)} problem(s)" if problems else "✓ the package has every part; now ask your peer to rerun it")
    return len(problems)


def rerun(pkg: Path) -> int:
    """The peer's command: rerun every logged step, then trace every headline number. Writes rerun_log.md."""
    con = U.con()
    log, claims = read_log(pkg), read_claims(pkg)
    lines = ["# Rerun log", "", "Rerun by: (the peer's name). Nothing was asked of the author or of an assistant.", "",
             "| Step | Same data | Logged headline | Rerun headline | Same |", "|---|---|---|---|---|"]
    heads = {}
    for rec in log:
        out = U.run_reply(U.reply_from(rec), con)
        same_data = all(U.fingerprint(con, t) == f for t, f in (rec.get("data") or {}).items())
        heads[rec["step"]] = out.headline
        lines.append(f"| {rec['step']} | {'yes' if same_data else 'NO'} | {rec.get('headline')} | {out.headline if not out.error else 'ERROR ' + out.error} | "
                     f"{'yes' if out.headline == rec.get('headline') else 'NO'} |")
    lines += ["", "| Headline number | Claimed | Rerun | Status |", "|---|---|---|---|"]
    failed = 0
    for c in claims:
        got = (heads.get(c.get("step")) or {}).get(c.get("key")) if c.get("step") else None
        if got is None:
            status = "no step"
        else:
            status = "matched" if abs(got - c["value"]) < 0.0005 else "drifted"
        failed += status != "matched"
        lines.append(f"| {c['name']} | {fmt(c['value'])} | {fmt(got)} | {status} |")
    verdict = "Reproduced: every headline number is reached from the log." if claims and not failed else \
        f"Not reproduced: {failed} of {len(claims)} headline numbers are not reached from the log."
    lines += ["", verdict, "", "Notes from the peer: (what you had to guess, and anything the log does not explain)"]
    text = "\n".join(lines) + "\n"
    print(text)
    try:
        (pkg / "rerun_log.md").write_text(text, encoding="utf-8")
    except OSError as e:
        print(f"(rerun_log.md was not written: {e})")
    return failed


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("readme", "check", "rerun"):
        raise SystemExit(__doc__)
    folder = Path(sys.argv[2])
    if not folder.exists():
        raise SystemExit(f"no such folder: {folder}")
    if sys.argv[1] == "readme":
        readme(folder)
    else:
        sys.exit(1 if {"check": check, "rerun": rerun}[sys.argv[1]](folder) else 0)
