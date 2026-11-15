# Hudhud Parcel: definitions for analysis

Owner: Yasser Al-Madani, analytics lead. Every analysis states which definition it uses.

## On time

- **D-1 (deliveries created before 1 April 2026).** A parcel is on time when it is delivered on or before its
  promised date. Parcels that were never delivered are not counted.
- **D-2 (deliveries created on or after 1 April 2026).** A parcel is on time when it is delivered at or before
  `promised_by`: the promised date at the service's cut-off hour (standard 18, express 13). A dispatched parcel
  that was never delivered (status failed or returned) counts as late.
- `deliveries.on_time_flag` is written by the operations system with the definition in force when the parcel
  was created. It is empty for cancelled orders, and for undelivered parcels created under D-1.
- **For any comparison across the year, apply D-2 to every month.** D-2 can be computed for the whole year
  from `delivered_at` and `promised_by`.

## Denominator

- The on-time rate is on-time parcels divided by **dispatched** parcels: status delivered, failed or returned.
- Cancelled orders never left a hub: they are in no rate.
- Test shipments are deliveries of customers whose `segment` is `TEST`. They are in no rate.

## Grain

| Table | One row is | Key |
|---|---|---|
| deliveries | one parcel | delivery_id |
| scans | one delivery attempt scan; handhelds can upload a scan twice | scan_id |
| route_plans | one version of one route's plan for one day | plan_id; the plan in force is the highest version |
| driver_shifts | one shift; a driver on a split shift has two rows that day | driver_id, shift_date, shift_no |
| complaints | one complaint, with the category the care agent chose | complaint_id |
| customers, drivers, hubs | one customer, driver, hub | their id |

## Time

- `created_at`, `promised_by`, `delivered_at` are local time (Asia/Riyadh).
- `scans.scan_time_utc` is UTC: local time minus three hours.
- A delivery belongs to the month of `created_at`.
