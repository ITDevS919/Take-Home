# AI Usage Documentation

## Tools Used

- ChatGPT (GPT-5.3)
- Used for:
  - Architecture planning
  - Test design
  - Documentation drafting

---

## Example Prompts

- "Design incremental ingestion pipeline with checkpoint safety"
- "How to implement deterministic search without embeddings"
- "Write pytest tests for idempotent ingestion system"

---

## What AI Helped With

- Structuring the project
- Structuring test scenarios:
  - checkpoint correctness
  - idempotency
  - dry-run behavior
  - failure safety
- Drafting documentation content and formatting
- Improving clarity and organization of written explanations


---

## What Was Implemented Manually

- Database schema and seed data (`init.sql`, `changes.sql`)
- Incremental ingestion logic (`updated_at > checkpoint`)
- Checkpoint management and atomic updates
- JSONL lake writing and directory structure
- Event emission logic
- Deterministic search implementation (hash-based vectorization)
- API endpoints (`/ingest`, `/search`)
- Debugging and fixing runtime issues

---

## What Was Manually Verified

- SQL schema correctness
- Incremental query logic (`updated_at > checkpoint`)
- Atomic checkpoint behavior
- File system operations (temp + rename)
- Event emission format
- Search determinism (same query → same result)
- Test reliability

---

## Corrections Made

- Fixed database connection issue (local DB vs Docker DB)
- Resolved permission issues (`TRUNCATE` privilege)
- Adjusted test client behavior (`raise_server_exceptions=False`)
- Ensured deterministic ordering (tie-break by `case_id`)
- Fixed import path issues for pytest

---

## Tradeoffs

### Simplicity vs Production Readiness
- Used full index rebuild instead of incremental updates
- Used local filesystem instead of distributed storage (e.g., S3)

### Deterministic Search vs Semantic Accuracy
- Implemented hash-based vectorization instead of embeddings
- Ensures reproducibility but does not capture deep semantics

---

## Final Confidence

High confidence in:
- correctness
- determinism
- idempotency
- test coverage

Known limitations:
- not optimized for large-scale datasets
- not a distributed production system

High confidence in:
- correctness
- determinism
- idempotency
- test coverage

Known limitations:
- not optimized for large-scale data
- not production distributed system