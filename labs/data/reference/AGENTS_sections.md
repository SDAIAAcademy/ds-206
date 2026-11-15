
## Definitions

- On time is D-2 for every month: `delivered_at <= promised_by`. A dispatched parcel never delivered is late.
- Never use `on_time_flag` for a comparison across months: it mixes two definitions.
- The denominator is dispatched parcels: status delivered, failed or returned. Cancelled orders are in no rate.
- Test shipments (customers with segment TEST) are in no rate.
- A parcel belongs to the month of `created_at`.
- All times are local except `scans.scan_time_utc`, which is UTC (local minus three hours).

## Checks

- Before answering, show the row count of the working table and of the result.
- A monthly table has exactly 12 rows, 2025-10 to 2026-09.
- Its deliveries sum to the number of dispatched, non-test parcels.

## Do not

- Do not join `scans` to count parcels: scans can be uploaded twice.
- Do not print rows of `complaints`, `drivers` or `customers`.
- Do not round before the last step.
