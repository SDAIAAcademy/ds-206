"""Helpers shared by every lab of Analysis with AI Assistants (DS-206).

The case: Hudhud Parcel, a fictional courier in Riyadh, Jeddah, Dammam and Madinah. All data is synthetic
(prepare_data.py, seed 206) and is built on first use into labs/artifacts/hudhud/.

    import hudhud as U
    con = U.con()                                  # DuckDB with one view per table
    reply = U.recorded("1.1", "one_line")          # a recorded reply of Rafiq, the notebook assistant
    out = U.run_reply(reply, con)                  # runs the reply's code: out.result, out.headline, out.error
    live = U.ask("What is our on-time rate?")      # the same request to a free hosted model, when a key is set
    U.note("1.1", produced=..., checked=..., wrong=...)   # the verification note every lab ends with
    U.check(cond, "what is true")                  # prints a tick, or stops with what went wrong
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
ART = LABS / "artifacts"
STORE = ART / "hudhud"
QUICK = os.getenv("HUDHUD_QUICK", "0") == "1"
TABLES = ["hubs", "customers", "drivers", "driver_shifts", "route_plans", "deliveries", "scans", "complaints"]
CHANGE_DAY = "2026-04-01"       # the day the on-time definition changed
MODEL = os.getenv("HUDHUD_MODEL", "google/gemma-4-31b-it:free")
BASE_URL = os.getenv("HUDHUD_BASE_URL", "https://openrouter.ai/api/v1")


def pick(full, quick):
    """The small value in quick mode (HUDHUD_QUICK=1), the full one otherwise."""
    return quick if QUICK else full


def check(cond, msg: str) -> None:
    if not cond:
        raise AssertionError("✗ " + msg)
    print("✓", msg)


# ------------------------------------------------------------------ data
def ensure_data() -> Path:
    """Build the synthetic tables once (about 20 seconds); rebuild when the generator changed."""
    import prepare_data as G
    meta = STORE / "meta.json"
    if meta.exists() and json.loads(meta.read_text(encoding="utf-8")).get("generator") == G.fingerprint():
        return STORE
    print("Building the Hudhud tables (once, about 20 seconds) ...")
    G.write(STORE)
    return STORE


def con():
    """A DuckDB connection with one view per table. Timestamps are local time, except scans.scan_time_utc."""
    import duckdb
    store = ensure_data()
    c = duckdb.connect()
    for t in TABLES:
        c.execute(f"CREATE VIEW {t} AS SELECT * FROM read_parquet('{(store / (t + '.parquet')).as_posix()}')")
    return c


def reference(name: str | None = None):
    """A planted answer, computed by the generator with pandas (never by the labs' SQL)."""
    ref = json.loads((ensure_data() / "reference.json").read_text(encoding="utf-8"))
    return ref if name is None else ref[name]


def load(name: str):
    """A supplied file of the case study from labs/data/: .json, .jsonl, .md, .sql or .py."""
    p = DATA / name
    text = p.read_text(encoding="utf-8")
    if p.suffix == ".json":
        return json.loads(text)
    if p.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return text


def schema_text(c=None, tables: list[str] | None = None) -> str:
    """Table and column names with types: what an assistant is shown in place of rows."""
    c = c or con()
    out = []
    for t in tables or TABLES:
        cols = c.execute(f"DESCRIBE {t}").fetchall()
        out.append(f"{t}(" + ", ".join(f"{name} {typ}" for name, typ, *_ in cols) + ")")
    return "\n".join(out)


# ------------------------------------------------------------------ the assistant
SYSTEM = """You are Rafiq, a coding assistant inside an analyst's notebook at a courier company.
A DuckDB connection named `con` is open. You see table and column names only, never rows.
Reply with at most four sentences, then exactly one ```python code block. The code uses `con.sql(...).df()`,
sets `result` to a pandas DataFrame and `headline` to a dict of named numbers. Do not print rows of data."""


@dataclass
class Reply:
    """One reply of the assistant: its words, its code, and what produced it."""
    text: str
    code: str
    request: str = ""
    context: str = ""
    model: str = "scripted stand-in"
    settings: dict = field(default_factory=dict)
    name: str = ""
    live: bool = False


@dataclass
class Outcome:
    result: Any = None
    headline: dict = field(default_factory=dict)
    error: str = ""


def recorded(lab: str, name: str | None = None):
    """A recorded reply for a lab (or all of them, by name). The recordings are scripted for the course:
    written to carry the choices and errors this course teaches, not captured from one product."""
    items = {k: Reply(name=k, **v) for k, v in load(f"recorded/lab_{lab.replace('.', '_')}.json").items()}
    return items if name is None else items[name]


def has_key() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY") or os.getenv("HUDHUD_API_KEY"))


def ask(request: str, context: str = "", *, temperature: float = 0.7, seed: int | None = None,
        model: str | None = None, tables: list[str] | None = None, c=None) -> Reply | None:
    """Send a request to a free hosted model (OpenRouter by default). Only the schema of `tables` leaves the
    notebook, never rows. Returns None, with one line saying why, when there is no key or the host fails."""
    key = os.getenv("OPENROUTER_API_KEY") or os.getenv("HUDHUD_API_KEY")
    if not key:
        print("No key set (OPENROUTER_API_KEY): continuing with the recorded reply.")
        return None
    settings = {"temperature": temperature, **({"seed": seed} if seed is not None else {})}
    system = SYSTEM + "\n\nTables:\n" + schema_text(c, tables) + (("\n\nProject context file:\n" + context) if context else "")
    body = {"model": model or MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": request}], **settings}
    req = urllib.request.Request(BASE_URL.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            text = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"] or ""
    except (urllib.error.URLError, KeyError, IndexError, TimeoutError, json.JSONDecodeError) as e:
        print(f"The hosted model did not answer ({type(e).__name__}: {e}): continuing with the recorded reply.")
        return None
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    return Reply(text=text[: m.start()].strip() if m else text, code=m.group(1).strip() if m else "", request=request,
                 context=context, model=model or MODEL, settings=settings, live=True)


def run_reply(reply: Reply, c=None) -> Outcome:
    """Run a reply's code against the data. The code sees `con` and `pd`; it sets `result` and `headline`."""
    space: dict = {"con": c or con(), "pd": pd}
    try:
        exec(reply.code, space)                      # noqa: S102 - running the assistant's code is the lab
    except Exception as e:                           # the error is data for the lab, not a crash
        return Outcome(error=f"{type(e).__name__}: {e}")
    head = space.get("headline") or {}
    return Outcome(result=space.get("result"), headline={k: (round(float(v), 4) if isinstance(v, (int, float)) else v) for k, v in head.items()})


def show(reply: Reply, width: int = 110) -> None:
    print(f"[{reply.model}{' · live' if reply.live else ' · recorded'}] {reply.text}\n" + "-" * width)
    print(reply.code)


def similarity(a: str, b: str) -> float:
    """How alike two pieces of code are, 0 to 1, ignoring blank lines and indentation."""
    norm = lambda s: [ln.strip() for ln in s.splitlines() if ln.strip()]
    return round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 2)


# ------------------------------------------------------------------ briefs, context files, notes
BRIEF_PARTS = ["question", "data", "definitions", "constraints", "acceptance_checks"]
CONTEXT_PARTS = {"Data": r"^#+\s*data", "Definitions": r"^#+\s*definitions", "Conventions": r"^#+\s*conventions",
                 "Checks": r"^#+\s*checks", "Do not": r"^#+\s*do not"}


def brief_gaps(brief: dict) -> list[str]:
    """What a delegation brief lacks: a missing part, a part too short to act on, fewer than three checks."""
    gaps = [f"missing: {p}" for p in BRIEF_PARTS if not brief.get(p)]
    gaps += [f"too short to act on: {p}" for p in BRIEF_PARTS[:4] if brief.get(p) and len(str(brief[p]).split()) < 6]
    checks = brief.get("acceptance_checks") or []
    if checks and len(checks) < 3:
        gaps.append("fewer than three acceptance checks")
    gaps += [f"not a check a reviewer can apply: {c!r}" for c in checks
             if not re.search(r"\d|equal|every|no |none|one row|between|sum|match|only", str(c), re.I)]
    return gaps


def render_brief(brief: dict) -> str:
    lines = []
    for p in BRIEF_PARTS:
        v = brief.get(p, "")
        lines.append(f"## {p.replace('_', ' ').capitalize()}")
        lines += [f"- {c}" for c in v] if isinstance(v, list) else [str(v)]
    return "\n".join(lines)


def context_gaps(text: str) -> list[str]:
    """Sections a project context file should have and this one lacks."""
    return [name for name, pat in CONTEXT_PARTS.items() if not re.search(pat, text, re.I | re.M)]


def note(lab: str, *, produced: str, checked: str, wrong: str) -> str:
    """Write the verification note of a lab: what the assistant produced, how it was checked, what was wrong."""
    for label, value in (("produced", produced), ("checked", checked), ("wrong", wrong)):
        if len(str(value).split()) < 5:
            raise AssertionError(f"✗ the note's '{label}' needs a full sentence, with the number or the check in it")
    text = (f"# Verification note · Lab {lab}\n\n**What the assistant produced.** {produced}\n\n"
            f"**How it was checked.** {checked}\n\n**What was wrong.** {wrong}\n")
    out = ART / "notes"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"lab_{lab.replace('.', '_')}.md").write_text(text, encoding="utf-8")
    if os.getenv("HUDHUD_WRITE_REF", "0") == "1":      # the author's run keeps the note as the safety net's reference
        ref = DATA / "reference" / "notes.json"
        notes = json.loads(ref.read_text(encoding="utf-8")) if ref.exists() else {}
        notes[lab] = {"produced": produced, "checked": checked, "wrong": wrong}
        ref.write_text(json.dumps(dict(sorted(notes.items())), indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(text)
    return text


# ------------------------------------------------------------------ logs and packages
def sha(obj) -> str:
    """A short, stable fingerprint of a text or of anything that serialises to JSON."""
    text = obj if isinstance(obj, str) else json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:12]


LOG_FIELDS = ["step", "request", "context_sha", "model", "settings", "code", "data", "headline", "verified_by"]


def log_gaps(record: dict) -> list[str]:
    """Fields a rerun needs and this log record lacks."""
    gaps = [f for f in LOG_FIELDS if record.get(f) in (None, "", {}, [])]
    if record.get("settings") and "temperature" not in record["settings"]:
        gaps.append("settings.temperature")
    return gaps


DISCLOSURE_PARTS = {
    "tool": r"assistant|model",
    "steps": r"draft|wrote|generated|produced|summar",
    "data seen": r"schema|column names|rows|aggregate|no personal",
    "verification": r"recomput|checked|verified|reran|rerun",
    "accountability": r"responsib|accountab",
}


def disclosure_gaps(text: str) -> list[str]:
    """Parts a method and disclosure paragraph should state and this one does not."""
    return [name for name, pat in DISCLOSURE_PARTS.items() if not re.search(pat, text, re.I)]


# ------------------------------------------------------------------ small query helpers
def one(c, sql: str):
    """The single value a query returns (its first row, first column)."""
    return c.sql(sql).fetchall()[0][0]


def q(c, sql: str) -> pd.DataFrame:
    """A query's result as a DataFrame."""
    return c.sql(sql).df()


def reference_check(name: str, result: pd.DataFrame, c) -> tuple[bool, str]:
    """The three acceptance checks of Lab 1.3 for a monthly table (month, deliveries, on_time_rate)."""
    if name == "check_total":
        expected = one(c, """SELECT COUNT(*) FROM deliveries d JOIN customers k ON k.customer_id = d.customer_id
                             WHERE k.segment <> 'TEST' AND d.status <> 'cancelled'""")
        got = int(result["deliveries"].sum())
        return got == expected, f"table sums to {got:,}, dispatched non-test parcels are {expected:,}"
    if name == "check_months":
        want = [str(p) for p in pd.period_range("2025-10", "2026-09", freq="M")]
        got = list(result["month"])
        return got == want, f"{len(got)} rows, from {got[0]} to {got[-1]}"
    if name == "check_rates":
        r = result["on_time_rate"]
        jump = float(r.diff().abs().max())
        return bool(r.between(0, 1).all() and jump <= 0.05), f"rates {r.min():.3f} to {r.max():.3f}, largest month-to-month change {jump * 100:.1f} points"
    raise KeyError(name)


# ------------------------------------------------------------------ reference states for the safety nets
WRITE_REF = os.getenv("HUDHUD_WRITE_REF", "0") == "1"      # set by the course author when running the solutions


def keep(name: str, value) -> None:
    """Author's tool: store a solution's result as the reference a safety net loads. Does nothing in class."""
    if not WRITE_REF:
        return
    path = DATA / "reference" / name
    if path.suffix == ".json":
        value = json.dumps(value, indent=1, ensure_ascii=False, default=str) + "\n"
    path.write_text(value, encoding="utf-8", newline="\n")


# ------------------------------------------------------------------ charts
def draw(table: pd.DataFrame, spec: dict, name: str):
    """Draw a line chart from a spec (x, y, series, ylim, title) and save it under artifacts/charts/."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for key, part in table.groupby(spec["series"]):
        ax.plot(part[spec["x"]], part[spec["y"]], marker="o", markersize=3, label=str(key))
    if spec.get("ylim"):
        ax.set_ylim(*spec["ylim"])
    ax.set_title(spec.get("title", ""), loc="left", fontsize=11)
    ax.set_ylabel(spec["y"].replace("_", " "))
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.autofmt_xdate()
    out = ART / "charts"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"chart saved: artifacts/charts/{name}.png")
    return ax
