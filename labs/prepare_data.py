# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "duckdb>=1.1"]
# ///
"""The synthetic data of Hudhud Parcel, a fictional courier in four Saudi cities (DS-206).

    uv run prepare_data.py            # writes labs/artifacts/hudhud/*.parquet and reference.json

Seed 206, the same rows on every run. Nothing here describes a real person, driver, customer or
company: names, phone numbers and identity numbers are drawn from short invented lists and random
digits. The planted problems are listed in solutions/answer_key.md.

The labs do not call this file by hand: `hudhud.con()` builds the data on first use.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 206
N = 500_000
DAYS = 365                      # created 2025-10-01 .. 2026-09-30
PLAN_DAYS = DAYS + 8            # deliveries of the last days are attempted a few days later
D0 = np.datetime64("2025-10-01")
CHANGE = np.datetime64("2026-04-01")      # the on-time definition changed on this day
OPTIMISER = np.datetime64("2026-07-01")   # Dammam moved to optimiser-built route plans
CITIES = ["Riyadh", "Jeddah", "Dammam", "Madinah"]
HUBS = ["RUH-N", "RUH-S", "JED-N", "JED-S", "DMM-1", "MED-1"]
HUB_CITY = np.array([0, 0, 1, 1, 2, 3])
HUB_P = [0.21, 0.21, 0.15, 0.15, 0.17, 0.11]
ROUTES = 28
DRIVERS_PER_HUB = 150

FIRST = ["Adnan", "Bakr", "Daif", "Eid", "Fayez", "Ghanim", "Hamdan", "Ismail", "Jaber", "Karim", "Labib",
         "Mahdi", "Naif", "Obaid", "Rashid", "Salem", "Talal", "Umar", "Wadi", "Zaher"]
FAMILY = ["Al-Aswad", "Al-Bahri", "Al-Dabbagh", "Al-Fadl", "Al-Ghareeb", "Al-Hilali", "Al-Jabri", "Al-Kathiri",
          "Al-Lami", "Al-Mubarak", "Al-Nahdi", "Al-Oraini", "Al-Rifai", "Al-Sabban", "Al-Turki", "Al-Wabel"]
SHOP_A = ["Noor", "Rimal", "Sidra", "Lulu", "Ward", "Qamar", "Bayt", "Rawdah", "Dana", "Yasmin"]
SHOP_B = ["Trading", "Store", "Home", "Fashion", "Electronics", "Perfumes", "Books", "Kitchen", "Sports", "Gifts"]

AR = {
    "late": ["الشحنة رقم {id} تأخرت عن الموعد ولم يتواصل معي أحد.", "وعدتم بالتوصيل أمس والطرد {id} لم يصل حتى الآن.",
             "طلبي {id} متأخر يومين، أريد موعدا واضحا للتسليم.", "المندوب قال سيصل قبل المغرب ولم يأت، الشحنة {id}."],
    "damaged": ["استلمت الطرد {id} والكرتون مفتوح والمنتج مكسور.", "الشحنة {id} وصلت تالفة وأطلب تعويضا."],
    "wrong_address": ["تم تسليم الشحنة {id} إلى عنوان خاطئ.", "المندوب ذهب إلى حي آخر، الطرد {id} لم يصلني."],
    "driver_behaviour": ["المندوب رفض الصعود وطلب مني النزول، الشحنة {id}.", "أسلوب المندوب غير لائق عند تسليم الطرد {id}."],
    "refund_cod": ["دفعت نقدا عند الاستلام للشحنة {id} وأريد استرجاع المبلغ.", "المبلغ المطلوب عند الاستلام للطرد {id} أعلى من الفاتورة."],
    "other": ["أريد تغيير موعد استلام الشحنة {id}.", "كيف أتتبع الطرد {id}؟ الرابط لا يعمل."],
}
EN = {
    "late": ["Parcel {id} is late and nobody called me.", "You promised delivery yesterday and parcel {id} has not arrived.",
             "Order {id} is two days late. I need a firm delivery slot.", "The driver said before sunset and never came. Parcel {id}."],
    "damaged": ["Parcel {id} arrived with the box open and the item broken.", "Shipment {id} was damaged. I want compensation."],
    "wrong_address": ["Parcel {id} was delivered to the wrong address.", "The driver went to another district. Parcel {id} never reached me."],
    "driver_behaviour": ["The driver refused to come up and told me to come down. Parcel {id}.", "The driver was rude when handing over parcel {id}."],
    "refund_cod": ["I paid cash on delivery for parcel {id} and I want a refund.", "The cash amount asked for parcel {id} was higher than the invoice."],
    "other": ["I want to change the delivery slot of parcel {id}.", "How do I track parcel {id}? The link does not work."],
}
AR_TAIL = [" رقمي {phone}.", " اتصلوا بي على {phone}.", " الاسم {name}.", " أنا {name} ورقم جوالي {phone}."]
EN_TAIL = [" My number is {phone}.", " Call me on {phone}.", " Name: {name}.", " This is {name}, mobile {phone}."]
CATS = ["late", "damaged", "wrong_address", "driver_behaviour", "refund_cod", "other"]


def _phones(rng, n):
    return np.char.add("05", np.char.zfill(rng.integers(0, 10**8, n).astype(str), 8))


def build(n: int = N) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    day = np.timedelta64(1, "D")

    # ---- hubs, customers, drivers
    hubs = pd.DataFrame({"hub_id": HUBS, "city": [CITIES[c] for c in HUB_CITY],
                         "hub_name": ["Riyadh North", "Riyadh South", "Jeddah North", "Jeddah South", "Dammam", "Madinah"],
                         "sort_capacity_per_day": [42000, 40000, 30000, 28000, 32000, 20000]})
    nc = 3000
    seg = rng.choice(["marketplace", "sme", "individual"], nc, p=[0.08, 0.52, 0.40])
    customers = pd.DataFrame({
        "customer_id": [f"C{i:05d}" for i in range(1, nc + 1)],
        "customer_name": [f"{SHOP_A[i % 10]} {SHOP_B[(i // 10) % 10]} {i:04d}" for i in range(1, nc + 1)],
        "segment": seg,
        "contract_rate_sar": np.round(np.where(seg == "marketplace", rng.uniform(9, 13, nc), rng.uniform(14, 24, nc)), 2),
        "account_phone": _phones(rng, nc)})
    tests = pd.DataFrame({"customer_id": [f"C9999{i}" for i in range(5)], "customer_name": [f"QA TEST {i}" for i in range(5)],
                          "segment": "TEST", "contract_rate_sar": 0.0, "account_phone": "0500000000"})
    customers = pd.concat([customers, tests], ignore_index=True)

    nd = 6 * DRIVERS_PER_HUB
    drivers = pd.DataFrame({
        "driver_id": [f"DR{i:04d}" for i in range(nd)],
        "hub_id": np.repeat(HUBS, DRIVERS_PER_HUB),
        "full_name": [f"{FIRST[rng.integers(20)]} {FAMILY[rng.integers(16)]}" for _ in range(nd)],
        "national_id": np.char.add("1", np.char.zfill(rng.integers(0, 10**9, nd).astype(str), 9)),
        "phone": _phones(rng, nd),
        "contract": rng.choice(["staff", "contractor"], nd, p=[0.6, 0.4])})

    # ---- route plans: one final plan per hub, day and route, plus earlier versions for some
    stops = np.clip(rng.normal(45, 8, (6, PLAN_DAYS, ROUTES)), 20, 80).round().astype(int)
    opt_day = int((OPTIMISER - D0) / day)
    stops[4, opt_day:, :] = np.clip(rng.normal(63, 8, (PLAN_DAYS - opt_day, ROUTES)), 30, 90).round().astype(int)
    h, d, r = np.meshgrid(np.arange(6), np.arange(PLAN_DAYS), np.arange(ROUTES), indexing="ij")
    h, d, r = h.ravel(), d.ravel(), r.ravel()
    nver = rng.choice([1, 2, 3], h.size, p=[0.93, 0.06, 0.01])
    rep = np.repeat(np.arange(h.size), nver)
    ver = np.concatenate([np.arange(1, k + 1) for k in nver])
    final = ver == nver[rep]
    planned = np.where(final, stops.ravel()[rep], np.clip(stops.ravel()[rep] + rng.integers(-9, 10, rep.size), 15, 95))
    planner = np.where((h[rep] == 4) & (d[rep] >= opt_day), "optimiser", "manual")
    route_plans = pd.DataFrame({
        "plan_id": np.arange(1, rep.size + 1), "hub_id": np.array(HUBS)[h[rep]], "plan_date": (D0 + d[rep] * day),
        "route_id": np.char.add("R", np.char.zfill((r[rep] + 1).astype(str), 2)), "version": ver,
        "planned_stops": planned, "planner": planner})

    # ---- deliveries
    dates = D0 + np.arange(DAYS) * day
    dow = pd.DatetimeIndex(dates).day_of_week.to_numpy()          # Monday 0 .. Sunday 6
    w = np.where(dow == 4, 0.55, 1.0) * np.linspace(0.92, 1.08, DAYS)   # quieter Fridays, mild growth
    cday = np.sort(rng.choice(DAYS, n, p=w / w.sum()))
    csec = rng.integers(6 * 3600, 22 * 3600, n)
    hub = rng.choice(6, n, p=HUB_P)
    city = HUB_CITY[hub]
    express = rng.random(n) < 0.25
    pday = cday + np.where(express, 1, 2)
    cutoff = np.where(express, 13, 18) * 3600
    route = rng.integers(0, ROUTES, n)
    cust = rng.zipf(1.35, n) % nc
    is_test = rng.random(n) < 0.008
    cod = (rng.random(n) < 0.35) & ~is_test
    cod_amount = np.where(cod, np.round(rng.lognormal(5.0, 0.6, n), 0), 0.0)

    u = rng.random(n)
    status = np.select([u < 0.02, u < 0.04, u < 0.05], ["cancelled", "failed", "returned"], "delivered")
    status = np.where(is_test, "delivered", status)
    delivered = status == "delivered"

    long_route = (hub == 4) & (pday >= opt_day) & (stops[hub, pday, route] > 60)
    p_evening = np.where(long_route, 0.21, 0.07)
    v = rng.random(n)
    klass = np.select([v < 0.05, v < 0.05 + p_evening], ["next", "evening"], "ontime")
    klass = np.where(is_test, "ontime", klass)
    early = (klass == "ontime") & ~express & (rng.random(n) < 0.30)
    dday = pday + np.where(klass == "next", rng.integers(1, 4, n), 0) - early.astype(int)
    dsec = np.where(klass == "ontime", (8 * 3600 + rng.random(n) * (cutoff - 8 * 3600 - 60)).astype(int),
           np.where(klass == "evening", (cutoff + 60 + rng.random(n) * (22 * 3600 - cutoff - 120)).astype(int),
                    rng.integers(8 * 3600, 22 * 3600, n)))
    dsec = np.where(early, rng.integers(8 * 3600, 22 * 3600, n), dsec)

    extra = delivered & (rng.random(n) < np.where(cod, 0.12, 0.05))
    attempts = np.where(delivered, 1 + extra * rng.choice([1, 2], n, p=[0.8, 0.2]), 0)
    attempts = np.where(status == "failed", 3, np.where(status == "returned", 2, attempts))
    # a delivery with earlier attempts is delivered a day or two later than first planned
    dday = dday + np.where(delivered, attempts - 1, 0)
    last_day = np.where(delivered, dday, np.where(status == "failed", pday + 2, pday + 1))
    last_day = np.minimum(last_day, PLAN_DAYS - 1)
    dday = np.minimum(dday, PLAN_DAYS - 1)

    sec = np.timedelta64(1, "s")
    created_at = D0 + cday * day + csec * sec
    promised_date = D0 + pday * day
    promised_by = promised_date + cutoff * sec
    delivered_at = np.where(delivered, D0 + dday * day + dsec * sec, np.datetime64("NaT", "s"))
    new_rule = created_at >= CHANGE
    ok_old = delivered & ((D0 + dday * day) <= promised_date)
    ok_new = delivered & (delivered_at <= promised_by)
    flag = np.where(new_rule, ok_new.astype(float), np.where(delivered, ok_old.astype(float), np.nan))
    flag = np.where(status == "cancelled", np.nan, flag)

    drv_idx = hub * DRIVERS_PER_HUB + (route * 5 + last_day * 11) % DRIVERS_PER_HUB
    gone = status == "cancelled"
    delivery_id = 10_000_001 + np.arange(n)
    district = np.char.add(np.char.add(np.array(["RUH", "JED", "DMM", "MED"])[city], "-D"),
                           np.char.zfill(rng.integers(1, 13, n).astype(str), 2))
    deliveries = pd.DataFrame({
        "delivery_id": delivery_id,
        "customer_id": np.where(is_test, np.char.add("C9999", rng.integers(0, 5, n).astype(str)),
                                np.char.add("C", np.char.zfill((cust + 1).astype(str), 5))),
        "hub_id": np.array(HUBS)[hub], "city": np.array(CITIES)[city], "district": district,
        "service": np.where(express, "express", "standard"),
        "created_at": created_at, "promised_date": promised_date, "promised_by": promised_by,
        "status": status, "delivered_at": delivered_at, "attempts": attempts,
        "on_time_flag": pd.array(flag, dtype="Float64").astype("Int64"),
        "route_id": np.where(gone, None, np.char.add("R", np.char.zfill((route + 1).astype(str), 2))),
        "route_date": np.where(gone, np.datetime64("NaT", "s"), D0 + last_day * day),
        "driver_id": np.where(gone, None, drivers["driver_id"].to_numpy()[drv_idx]),
        "cod_amount": cod_amount, "weight_kg": np.round(rng.gamma(2.0, 1.4, n) + 0.1, 1),
        "recipient_phone": _phones(rng, n)})

    # ---- attempt scans (UTC = local time minus three hours); duplicates in Jeddah, March and April 2026
    parts = []
    idx = np.flatnonzero(delivered)
    parts.append((idx, attempts[idx], D0 + dday[idx] * day + dsec[idx] * sec, np.full(idx.size, "delivered")))
    for k in (1, 2):                                   # earlier attempts of delivered parcels
        idx = np.flatnonzero(delivered & (attempts > k))
        t = D0 + (dday[idx] - (attempts[idx] - k)) * day + rng.integers(9 * 3600, 21 * 3600, idx.size) * sec
        parts.append((idx, np.full(idx.size, k), t, rng.choice(["no_answer", "wrong_address", "refused"], idx.size, p=[0.6, 0.25, 0.15])))
    for k in (1, 2, 3):                                # attempts of failed and returned parcels
        idx = np.flatnonzero(~delivered & (attempts >= k))
        t = D0 + (pday[idx] + k - 1) * day + rng.integers(9 * 3600, 21 * 3600, idx.size) * sec
        out = np.where((status[idx] == "returned") & (k == 2), "refused", rng.choice(["no_answer", "wrong_address"], idx.size, p=[0.7, 0.3]))
        parts.append((idx, np.full(idx.size, k), t, out))
    si = np.concatenate([p[0] for p in parts]); sa = np.concatenate([p[1] for p in parts])
    st = np.concatenate([p[2] for p in parts]); so = np.concatenate([p[3] for p in parts])
    order = np.argsort(st, kind="stable")
    si, sa, st, so = si[order], sa[order], st[order], so[order]
    dup = (city[si] == 1) & (st >= np.datetime64("2026-03-01")) & (st < np.datetime64("2026-05-01")) & (so == "delivered") & (rng.random(si.size) < 0.35)
    si = np.concatenate([si, si[dup]]); sa = np.concatenate([sa, sa[dup]]); st = np.concatenate([st, st[dup]]); so = np.concatenate([so, so[dup]])
    scans = pd.DataFrame({"scan_id": 50_000_001 + np.arange(si.size), "delivery_id": delivery_id[si], "attempt_no": sa,
                          "scan_time_utc": st - np.timedelta64(3, "h"), "outcome": so,
                          "device_id": np.char.add(np.array(HUBS)[hub[si]], np.char.add("-H", np.char.zfill(((si * 7) % 40).astype(str), 2)))})

    # ---- driver shifts: one per driver and working day, 5% split in two
    hh, dd, rr = np.meshgrid(np.arange(6), np.arange(PLAN_DAYS), np.arange(ROUTES), indexing="ij")
    hh, dd, rr = hh.ravel(), dd.ravel(), rr.ravel()
    sd = hh * DRIVERS_PER_HUB + (rr * 5 + dd * 11) % DRIVERS_PER_HUB
    split = rng.random(sd.size) < 0.05
    rep = np.repeat(np.arange(sd.size), np.where(split, 2, 1))
    no = np.concatenate([np.arange(1, k + 1) for k in np.where(split, 2, 1)])
    total = rng.integers(8, 12, sd.size)
    driver_shifts = pd.DataFrame({
        "driver_id": drivers["driver_id"].to_numpy()[sd[rep]], "shift_date": D0 + dd[rep] * day, "shift_no": no,
        "start_hour": np.where(no == 1, rng.integers(7, 10, rep.size), 16),
        "hours": np.where(split[rep], np.where(no == 1, 5, total[rep] - 5), total[rep])})

    # ---- complaints: 20,000 texts; the export is sorted by channel, email first
    m = 20_000
    late_new = ~gone & ~is_test & ~ok_new
    wgt = np.where(gone | is_test, 0.0, 1.0) * np.where(late_new, 4.0, 1.0) * np.where(~delivered & ~gone, 1.5, 1.0) * np.where(city == 3, 1.6, 1.0)
    ci = np.sort(rng.choice(n, m, replace=False, p=wgt / wgt.sum()))
    channel = rng.choice(["app", "call", "email"], m, p=[0.55, 0.30, 0.15])
    ar_p = np.array([0.60, 0.58, 0.62, 0.88])[city[ci]]
    lang = np.where(channel == "email", np.where(rng.random(m) < 0.92, "en", "ar"), np.where(rng.random(m) < ar_p, "ar", "en"))
    p_late = np.array([0.72, 0.06, 0.05, 0.05, 0.07, 0.05]); p_fine = np.array([0.06, 0.30, 0.16, 0.13, 0.20, 0.15])
    p_mail = np.array([0.18, 0.50, 0.10, 0.05, 0.12, 0.05])
    uu = rng.random(m)
    cum = np.where((channel == "email")[:, None], p_mail.cumsum(), np.where(late_new[ci][:, None], p_late.cumsum(), p_fine.cumsum()))
    cat = np.array(CATS)[(uu[:, None] > cum).sum(axis=1).clip(0, 5)]
    tail = rng.random(m)
    texts = []
    for j in range(m):
        bank, tails = (AR, AR_TAIL) if lang[j] == "ar" else (EN, EN_TAIL)
        opts = bank[cat[j]]
        t = opts[(ci[j] + j) % len(opts)].format(id=delivery_id[ci[j]])
        if tail[j] < 0.42:
            k = int(tail[j] * 1000) % 4
            t += tails[k].format(phone="05" + f"{(ci[j] * 7919 + j) % 10**8:08d}", name=f"{FIRST[(ci[j] + j) % 20]} {FAMILY[j % 16]}")
        texts.append(t)
    complaints = pd.DataFrame({
        "complaint_id": 700_001 + np.arange(m), "delivery_id": delivery_id[ci],
        "created_date": D0 + np.minimum(last_day[ci] + rng.integers(0, 6, m), PLAN_DAYS + 5) * day,
        "city": np.array(CITIES)[city[ci]], "language": lang, "channel": channel, "category": cat, "text": texts})
    complaints["_k"] = complaints["channel"].map({"email": 0, "app": 1, "call": 2})
    complaints = complaints.sort_values(["_k", "complaint_id"], kind="stable").drop(columns="_k").reset_index(drop=True)

    return {"hubs": hubs, "customers": customers, "drivers": drivers, "route_plans": route_plans, "deliveries": deliveries,
            "scans": scans, "driver_shifts": driver_shifts, "complaints": complaints}


def reference(t: dict[str, pd.DataFrame]) -> dict:
    """The planted answers, computed here with pandas so the labs' SQL has an independent figure to meet."""
    d = t["deliveries"].merge(t["customers"][["customer_id", "segment"]], on="customer_id", how="left")
    real = d[d["segment"] != "TEST"]
    disp = real[real["status"] != "cancelled"].copy()
    disp["ok"] = (disp["delivered_at"] <= disp["promised_by"]).fillna(False)
    disp["month"] = disp["created_at"].dt.strftime("%Y-%m")
    disp["half"] = np.where(disp["created_at"] < pd.Timestamp("2026-04-01"), "before", "after")
    flag = d[d["on_time_flag"].notna()].assign(month=lambda x: x["created_at"].dt.strftime("%Y-%m"))
    sc = t["scans"]
    key = ["delivery_id", "attempt_no", "scan_time_utc", "outcome"]
    c = t["complaints"].merge(d[["delivery_id"]], on="delivery_id")
    per_city = disp.groupby("city").size()
    dq = disp[disp["city"] == "Dammam"].assign(q=lambda x: x["created_at"].dt.to_period("Q").astype(str))
    r4 = lambda x: round(float(x), 4)
    return {
        "rows": {k: int(len(v)) for k, v in t.items()},
        "n_test": int((d["segment"] == "TEST").sum()), "n_cancelled": int((real["status"] == "cancelled").sum()),
        "n_dispatched": int(len(disp)), "n_dup_scans": int(sc.duplicated(key).sum()),
        "on_time": r4(disp["ok"].mean()),
        "on_time_by_city": {k: r4(v) for k, v in disp.groupby("city")["ok"].mean().items()},
        "on_time_by_half": {k: r4(v) for k, v in disp.groupby("half")["ok"].mean().items()},
        "on_time_by_month": {k: r4(v) for k, v in disp.groupby("month")["ok"].mean().items()},
        "late_count_by_city": {k: int(v) for k, v in (~disp["ok"]).groupby(disp["city"]).sum().items()},
        "dammam_by_quarter": {k: r4(v) for k, v in dq.groupby("q")["ok"].mean().items()},
        "flag_rate": r4(flag["on_time_flag"].astype(float).mean()),
        "flag_rate_all_rows": r4(d["on_time_flag"].fillna(0).astype(float).mean()),
        "flag_by_month": {k: r4(v) for k, v in flag.groupby("month")["on_time_flag"].apply(lambda s: s.astype(float).mean()).items()},
        "complaints_by_category": {k: int(v) for k, v in c["category"].value_counts().items()},
        "complaints_per_1000": {k: round(float(v), 2) for k, v in (c.groupby("city").size() / per_city * 1000).items()},
    }


def write(out: Path) -> dict:
    import duckdb
    out.mkdir(parents=True, exist_ok=True)
    tables = build()
    con = duckdb.connect()
    for name, df in tables.items():
        con.register("df_" + name, df)
        target = (out / f"{name}.parquet").as_posix()
        con.execute(f"COPY (SELECT * FROM df_{name}) TO '{target}' (FORMAT parquet)")
    ref = reference(tables)
    (out / "reference.json").write_text(json.dumps(ref, indent=1), encoding="utf-8")
    (out / "meta.json").write_text(json.dumps({"generator": fingerprint(), "seed": SEED}), encoding="utf-8")
    return ref


def fingerprint() -> str:
    return hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:16]


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "artifacts" / "hudhud"
    ref = write(target)
    print(json.dumps({k: ref[k] for k in ("rows", "n_test", "n_dup_scans", "on_time", "on_time_by_city", "on_time_by_half",
                                          "dammam_by_quarter", "flag_rate", "complaints_per_1000")}, indent=1))
