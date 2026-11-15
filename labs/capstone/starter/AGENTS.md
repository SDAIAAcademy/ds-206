# Project context: Hudhud Parcel, (your question)

## Data

- DuckDB tables; one row of `deliveries` is one parcel. All data is synthetic.
- (grain and keys of every table you use)

## Definitions

- On time: D-2 for every month (delivered at or before `promised_by`; dispatched and never delivered is late).
- Denominator: dispatched parcels of real customers. No cancelled orders, no customers of segment TEST.

## Rules for the assistant

- State every assumption you make before the code.
- Report rows before and after every join.
- (your own rules)

## Handling

- Only table and column names may be sent to a hosted model. No rows, samples or example values.
