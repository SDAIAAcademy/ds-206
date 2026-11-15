# Late-delivery analysis: context for assistants

This file is read by the notebook assistant before every request in this project.

## Data

- DuckDB connection `con` with the views hubs, customers, drivers, driver_shifts, route_plans, deliveries,
  scans and complaints.
- You are shown table and column names, never rows.

## Conventions

- SQL through `con.sql(...).df()`. One query per step, common table expressions over nested subqueries.
- Rates as fractions between 0 and 1, rounded only for display.
- Set `result` to the table and `headline` to a dict of the numbers a reader will quote.
