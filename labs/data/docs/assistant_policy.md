# Hudhud Parcel: policy on AI assistants in analysis

Owner: Sawsan Al-Fraih, data protection officer. This is the policy of a fictional company, written for
this course. It applies the four national classification levels and takes the strict reading of the
national generative AI guidelines for anything that leaves the company.

## Levels

Hudhud classifies every table as Public, Restricted, Secret or Top Secret. It holds no Secret or Top
Secret data. A table that has not been classified is treated as Restricted.

- **P-1.** A table takes the level of its most sensitive column.
- **P-2.** A column that identifies or describes a person (a name, a phone number, an identity number,
  a recipient's district, a driver's hours, free text written by a customer) is personal data and makes its
  table Restricted. So does a commercial column (a contract rate, a route plan).
- **P-3.** An aggregate may be classified Public by its data owner when it has no personal column and no
  cell built from fewer than 20 parcels.

## Destinations

- **Hosted assistant**: a model served by a company other than Hudhud. Requests leave Hudhud.
- **Local assistant**: a model served on Hudhud's own machines. Nothing leaves Hudhud.
- **Neither**: no assistant sees the rows.

- **P-4.** A hosted assistant receives rows of Public data only.
- **P-5.** Table and column names (the schema) of any table may be shown to a hosted assistant.
  Rows, samples and example values of a Restricted table may not.
- **P-6.** Rows of a Restricted table may go to the local assistant, limited to the columns the task needs.
- **P-7.** A table that holds a government identity number goes to no assistant. Analysis that needs it
  uses a view without that column.
- **P-8.** Every request is logged: what was sent, to which assistant, by whom.

## Who decides

The data owner of each table classifies it. The analyst applies this policy before the first request and
records the result in the project's data-handling table.
