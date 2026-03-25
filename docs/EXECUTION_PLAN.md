# Execution Plan

## Objective

Implement a deterministic, incremental ingestion pipeline with search capability within ~2–3 hours.

---

## Implementation Order

1. Docker + PostgreSQL setup
2. Schema + seed data (`init.sql`)
3. Incremental change script (`changes.sql`)
4. DB access layer
5. Checkpoint management
6. Ingest pipeline
7. Lake writer
8. Event emitter
9. Search engine
10. API endpoints
11. Tests
12. Documentation

---

## Time Allocation

| Task | Time |
|------|------|
| DB setup | 20 min |
| Ingest logic | 40 min |
| Search | 20 min |
| Tests | 25 min |
| Docs | 20 min |

---

## Testing Strategy

- Unit + integration style tests
- Validate:
  - checkpoint progression
  - idempotency
  - dry run correctness
  - deterministic search

---

## Risks

| Risk | Mitigation |
|------|-----------|
| DB connection issues | use env config |
| nondeterministic search | fixed hashing |
| partial writes | atomic file replace |
| checkpoint corruption | update last |

---

## Completion Criteria

- All endpoints working
- Tests passing
- Docs complete
- Deterministic behavior verified