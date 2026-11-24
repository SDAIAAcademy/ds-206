# Answer key

The numbers every lab should reach, on the tables built from seed 206. The solution notebooks in this
folder hold the code. All figures were computed on the course's own synthetic data.

## Day 1

- **1.1** The one-line reply says 85.3% (0.8533). It made six assumptions: the system flag as the
  definition, a join to scans, delivered parcels only, test shipments kept, the year pooled, cities and
  services pooled. Six defensible variants give 0.8916, 0.8533, 0.8394, 0.8384, 0.8194 and 0.7942: a
  range of 9.7 points. The rate under the definitions document is **0.7942** (486,078 dispatched parcels).
- **1.2** Reference marking of the ten steps: keep 1, 7, 10; delegate 2, 5, 9; assist 3, 4, 6, 8.
  Eight of ten matching the reference passes; a different mark with a sound reason is discussed, not failed.
- **1.3** The first reply to the brief gives 0.7782 on 496,046 rows and fails the check on the total; the
  second gives 0.7942 on 486,078 and passes all three checks. The flag series jumps from 0.8941 in
  March to 0.7995 in April; under one definition the two months are 0.7991 and 0.7982.
- **1.4** Without the context file the reply is 7.3 points from the reference (0.8673); with it, 2.5
  points (0.8194). The context file narrowed the gap and did not close it: the reply still used
  delivered parcels as the denominator.

## Day 2

- **2.1** Dammam by quarter, recomputed: 0.7962, 0.8003, 0.7967, 0.7226. The assistant's series:
  0.8688, 0.8710, 0.8707, 0.8428. The bridge for the last quarter: definition -9.54 points, test
  shipments +0.04, undelivered parcels -2.31, duplicated scans -0.21.
- **2.2** Rows after each stage: 21,158, 22,699, 23,778, 21,620. Four errors: a fan-out on plan
  versions, a fan-out on split shifts, a date filter that drops the last day, and an inner join that
  drops parcels with no plan. Of 22,082 parcels in scope, 994, 688 and 236 are lost at three points.
  Corrected: short routes 0.7902 (8,462 parcels), long routes 0.6805 (13,620). The assistant reported
  0.8139 and 0.7026.
- **2.3** Late parcels per week: Riyadh 847, Dammam 464. Late rates: Riyadh 0.203, Dammam 0.277. The
  chart plots counts. Complaints: late delivery 7,288 (36%), damaged 4,516 (23%), Arabic 11,177 (56%).
  The summary read the first 500 rows of an export sorted by channel: all email, 92% English, 51%
  damaged. Madinah has 60.3 complaints per 1,000 parcels against 38.2 to 39.9 elsewhere. Late
  complaints from Dammam rise from 94 to 144 a month.
- **2.4** Five runs: the measure differs between runs; the worst city is Dammam in four runs and Riyadh
  in one, the run that counted parcels. Code similarity to the first run: 1.00, 0.82, 0.37, 0.73, 0.73.
  The variability table states which conclusions held in every run.

## Day 3

- **3.1** Hosted: `hubs` and the aggregate of on-time rate by city and month. Neither: `drivers`.
  Local: the other seven items. 31.5% of complaint texts carry a mobile number. Two of the six test
  requests are blocked: complaint rows to hosted (P-4) and driver rows to local (P-7).
  Stretch A: the pattern of task 3 used as it is gives 5 of the 10 known replies their verdict and lets
  5 through (a spaced mobile, a +966 mobile, a mobile in Arabic-Indic digits, two identity numbers). The
  reference screen gives all 10 their verdict with no false alarm: 4 pass, 4 masked, 2 blocked with two
  alerts that hold no value. The known cases are written by `_tools/make_known_replies.py`.
- **3.2** The helper lists what each of the three old records lacks. The new record lacks nothing; the
  rerun from the log line gives 0.7942 with matching fingerprints.
- **3.3** All three logged steps rerun on matching fingerprints. Trace: matched, matched, drifted
  (README 0.6841, log 0.6805), no step (144). The chart step has no verification recorded.
- **3.4** Three assisted steps, two verified. The found draft fails on eight points. A passing
  paragraph names the model in the log, the three steps, "table and column names only", how two steps
  were verified, that the weekly chart was not, and who is accountable.
