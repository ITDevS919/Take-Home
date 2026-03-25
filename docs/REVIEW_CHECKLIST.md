# Review Checklist

## Environment

- [ ] Docker starts PostgreSQL 16
- [ ] DB accessible on configured port
- [ ] Schema created correctly

---

## Data

- [ ] At least 30 customers seeded
- [ ] At least 200 cases seeded
- [ ] Keywords present for search relevance
- [ ] changes.sql produces deterministic updates

---

## Ingest

- [ ] Uses `updated_at > checkpoint`
- [ ] Dry run does not write or update state
- [ ] Real run writes lake files
- [ ] Events emitted per table
- [ ] Checkpoint updates only after success

---

## Idempotency

- [ ] Re-run without changes → zero deltas
- [ ] No duplicate rows in lake

---

## Atomicity

- [ ] Temp file + rename used
- [ ] Checkpoint written last
- [ ] Failure does not advance checkpoint

---

## Search

- [ ] Deterministic results
- [ ] Uses title + description
- [ ] Stable ordering (tie-breaker)

---

## Tests

- [ ] Ingest idempotency test
- [ ] Dry-run test
- [ ] Failure safety test
- [ ] Search determinism test

---

## Docs

- [ ] README complete
- [ ] AI usage documented
- [ ] Execution plan included
- [ ] AWS architecture provided