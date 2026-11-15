# Verification notes

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
