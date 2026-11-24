"""Known cases for screening the replies of the local assistant (Day 3, session 1).

    uv run python _tools/make_known_replies.py

Writes data/recorded/lab_3_1_known.json: ten replies of Rafiq, the local assistant, about Madinah
complaints, each with the verdict a correct screen gives (pass, mask or block). The replies are scripted
for the course; every number in them is invented from a fixed formula, like the data of prepare_data.py.

It also prints the figures of the parallel example on the slides (`known-cases-decide`,
`an-alert-without-the-value`): eight reply drafts for the Jeddah customer-care team, screened by three
candidate screens A, B and C. The slide example is not the lab's set, and screen C is not the lab answer
written out: it is one of three screens whose results the slide compares.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
AR = "٠١٢٣٤٥٦٧٨٩"


def phone(i: int) -> str:
    """An invented mobile number: 05 and eight digits from a fixed formula."""
    return "05" + f"{(i * 7919 + 4111) % 10**8:08d}"


def ident(i: int) -> str:
    """An invented identity number: 1 and nine digits from a fixed formula (the shape of drivers.national_id)."""
    return "1" + f"{(i * 104729 + 2207) % 10**9:09d}"


def spaced(p: str) -> str:
    return f"{p[:3]} {p[3:6]} {p[6:]}"


def intl(p: str, prefix: str = "+966") -> str:
    return f"{prefix} {p[1:3]} {p[3:6]} {p[6:]}"


def arabic(s: str) -> str:
    return s.translate(str.maketrans("0123456789", AR))


# ------------------------------------------------------------------ the lab's set: Madinah, ten replies
LAB = [
    ("k01", "pass", "Of 412 Madinah complaints in September, 151 are about late delivery and 88 about a missed call before arrival."),
    ("k02", "mask", f"The most repeated complaint is from a customer who asks to be called back on {phone(1)} about two missed attempts."),
    ("k03", "mask", f"أكثر الشكاوى تكرارًا من عميل يطلب الاتصال به على {spaced(phone(2))} بعد محاولتي تسليم فاشلتين."),
    ("k04", "mask", f"Three complaints quote the same mobile, {intl(phone(3))}, and all three concern one district."),
    ("k05", "mask", f"تذكر إحدى الشكاوى رقم الجوال {arabic(phone(4))} وتطلب تغيير موعد التسليم."),
    ("k06", "block", f"The late parcels of the week cluster on one driver, identity number {ident(1)}, on the evening shift."),
    ("k07", "mask", f"Two customers left numbers in their complaints: {phone(5)} and {phone(6)}."),
    ("k08", "pass", "On 05/04/2026, 37 parcels missed their promised day, against a September daily average of 22."),
    ("k09", "pass", "أغلب الشكاوى المكتوبة بالعربية تخص التأخير، وأقلها يخص تلف الطرود."),
    ("k10", "block", f"تتكرر الشكاوى على مندوب واحد رقم هويته {arabic(ident(2))} في الوردية المسائية."),
]

# ------------------------------------------------------------------ the slides' set: Jeddah care, eight drafts
SLIDE = [
    ("j1", "pass", "No phone or identity number", "Thank you for your patience: your parcel left the Jeddah South hub this morning."),
    ("j2", "mask", "A mobile, written plain", f"We tried to reach you on {phone(11)} twice and will try again tomorrow."),
    ("j3", "mask", "A mobile, with dashes", f"Our driver will call {phone(12)[:3]}-{phone(12)[3:6]}-{phone(12)[6:]} before arriving."),
    ("j4", "mask", "A mobile, with 00966", f"Please confirm that {intl(phone(13), '00966')} is still your number."),
    ("j5", "block", "A driver's identity number", f"The driver on your route, identity number {ident(11)}, has been informed."),
    ("j6", "pass", "A date then a count", "On 05/03/2026, 14 parcels on your street were delayed by road works."),
    ("j7", "pass", "Counts in Arabic digits", f"وصلتنا {arabic('42')} شكوى هذا الأسبوع وعالجنا {arabic('39')} منها."),
    ("j8", "block", "An identity number, spaced", f"Identity number {ident(12)[0]} {ident(12)[1:4]} {ident(12)[4:7]} {ident(12)[7:]} appears on the shift sheet."),
]

PHONE = re.compile(r"05\d{8}")
IDENT = re.compile(r"(?<!\d)[12]\d{9}(?!\d)")


def screen_a(text: str) -> str:
    """A: the patterns as they are, on the text as it is."""
    if IDENT.search(text):
        return "block"
    return "mask" if PHONE.search(text) else "pass"


def screen_b(text: str) -> str:
    """B: digits made Western, then every non-digit between two digits removed."""
    t = re.sub(r"(?<=\d)\D{1,3}(?=\d)", "", text.translate(str.maketrans(AR, "0123456789")).replace("+966", "0").replace("00966", "0"))
    if IDENT.search(t):
        return "block"
    return "mask" if PHONE.search(t) else "pass"


def screen_c(text: str) -> str:
    """C: digits made Western, the country code read as 0, spaces and dashes inside a number removed."""
    t = text.translate(str.maketrans(AR, "0123456789"))
    t = re.sub(r"(?:\+|00)966[ -]?(?=5)", "0", t)
    t = re.sub(r"(?<=\d)[ -](?=\d)", "", t)
    if IDENT.search(t):
        return "block"
    return "mask" if PHONE.search(t) else "pass"


def tally(rows, verdicts):
    personal = [r for r in rows if r[1] != "pass"]
    clean = [r for r in rows if r[1] == "pass"]
    return {
        "right": sum(v == r[1] for r, v in zip(rows, verdicts)),
        "missed": sum(r[1] != "pass" and v == "pass" for r, v in zip(rows, verdicts)),
        "false_alarms": sum(r[1] == "pass" and v != "pass" for r, v in zip(rows, verdicts)),
        "personal": len(personal), "clean": len(clean),
    }


def main() -> None:
    out = LABS / "data" / "recorded" / "lab_3_1_known.json"
    cases = [{"id": i, "expected": e, "text": t} for i, e, t in LAB]
    out.write_text(json.dumps(cases, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(LABS).as_posix()}: {len(cases)} known cases")

    print("\nSlide example, Jeddah care drafts:")
    print(f"{'case':5s} {'expected':8s} {'A':6s} {'B':6s} {'C':6s} what it holds")
    va, vb, vc = ([f(r[3]) for r in SLIDE] for f in (screen_a, screen_b, screen_c))
    for r, a, b, c in zip(SLIDE, va, vb, vc):
        print(f"{r[0]:5s} {r[1]:8s} {a:6s} {b:6s} {c:6s} {r[2]}")
    for name, v in (("A", va), ("B", vb), ("C", vc)):
        print(name, tally(SLIDE, v))


if __name__ == "__main__":
    main()
