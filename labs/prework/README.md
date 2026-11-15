# Pre-work: two hours before Day 1

The course assumes you write SQL joins and dataframe group-bys without help. The pre-work checks that,
and lets you repair a gap with an assistant used as a tutor.

## 1 · Setup (20 minutes)

Run `00_setup_check.ipynb`. It builds the tables and tells you whether your machine is ready.

## 2 · The entry quiz (30 minutes, no assistant)

Answer in a notebook opened in `labs/`, after the setup cell of any lab. Write the SQL yourself. The
expected results are at the bottom of this page; look only after you have a number.

1. How many rows does `deliveries` have, and how many distinct `delivery_id`?
2. How many deliveries does each `status` have?
3. Join `deliveries` to `customers`. How many deliveries belong to customers of segment `TEST`?
4. Join `deliveries` to `scans` on `delivery_id` and count the rows. Why is it more than the number of deliveries?
5. Which city has the most deliveries, and which the fewest?
6. With pandas: load `SELECT city, service, weight_kg FROM deliveries` and compute the mean weight by city and service. How many rows does the result have?

If a question took more than five minutes, use the next part on that topic.

## 3 · An assistant as a tutor (60 minutes)

The pre-work is AI-tutor: the assistant explains and asks, and you write. Paste this instruction at the
start of a conversation with any assistant you are allowed to use, then work on the topics you missed.

> Act as a tutor for SQL and pandas. I am preparing for a course and must be able to write joins and
> group-bys without help. Do not write the solution to my exercise. Ask me what I expect the result to
> be before I run anything. When my query is wrong, tell me which clause to look at, not the fix. Use
> small invented tables of five rows for your explanations. After each topic, give me one exercise and
> wait for my answer.

Topics worth an hour: the grain of a table and what a join does to row counts; a left join against an
inner join; `COUNT(*)` against `COUNT(DISTINCT ...)`; a group-by with a filtered average; reading a
timestamp as a date.

Describe tables to the tutor by their column names. Do not paste rows of data from your workplace.

## 4 · Write down one thing (10 minutes)

One sentence for Day 1: a number in your own work that an assistant helped produce, and how you know it
is right.

## Expected results of the quiz

1. 500,000 rows and 500,000 distinct ids: one row is one parcel.
2. delivered 475,053; cancelled 9,968; failed 9,960; returned 5,019.
3. 3,954.
4. 565,680 rows: a parcel has one scan per delivery attempt, and some scans were uploaded twice.
5. Riyadh the most (210,077), Madinah the fewest (55,186).
6. Eight rows: four cities by two services.

## The follow-up task, after the course

Within four weeks: one assisted analysis at work, or on open data, with a verification note for each
headline number, sent to your trainer. Use the package layout of the capstone. Work data stays under
your organisation's own rules: when in doubt, use open data.
