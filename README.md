# Mini Data Interop + Event Sync + AI-Ready Search

This project implements a deterministic, incremental data ingestion pipeline with local lake output, event emission, and a deterministic in-memory search service.

---

## 🚀 Features

- Incremental ingestion using checkpoint watermark
- Deterministic JSONL lake output (idempotent)
- Event emission (stdout JSON)
- Deterministic search (hash-based vectorization)
- Atomic checkpoint updates
- Automated tests for ingestion correctness and search determinism

---

## 🧱 Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL 16 (Docker)
- psycopg
- pytest

---

## ⚙️ Setup Instructions

### 1. Start PostgreSQL

```bash
docker compose up -d

```

Default DB config:
host: localhost
port: 5433
db: interop
user: interop
password: interop

### 2. Setup Python Environment

```bash
python -m venv .venv
source .venv/bin/activate  # or Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Run the Service

```bash
uvicorn app.main:app --reload

```


## 📡 API Usage

- Ingest (Dry Run)
    curl -X POST "http://localhost:8000/ingest?dry_run=true"

- Ingest (Real Run)
    curl -X POST "http://localhost:8000/ingest?dry_run=false"

- Search
    curl -X POST "http://localhost:8000/search" \
    -H "Content-Type: application/json" \
    -d '{"query":"billing fraud aml","top_k":5}'

## 🧪 Run Tests

```bash
pytest -q

```

## 📂 Output Structure

- Lake
    ./lake/customers/date=YYYY-MM-DD/data.jsonl
    ./lake/cases/date=YYYY-MM-DD/data.jsonl

- Checkpoint
    ./state/checkpoint.json

- Events
    stdout (JSON per table)

## 🧠 Design Decisions

- Incremental Ingestion
    Uses strict updated_at > checkpoint
    Ensures no duplicate processing
- Idempotency
    Lake files are overwritten per run
    No duplicate rows on re-run
- Atomicity
    Temp file write → rename
    Checkpoint updated only after full success
- Deterministic Search
    Token hashing into fixed vector space
    No randomness
    Stable ranking with tie-breaker

## ⚠️ Assumptions
    
- Single-node local filesystem (no distributed FS)
- Dataset size small enough for full in-memory search index
- No concurrent ingest runs

## 🧪 What is Tested

- Checkpoint correctness and idempotency
- Dry-run behavior
- Failure safety (checkpoint does not advance)
- Search determinism

## 🛠️ Future Improvements

- Streaming ingestion (CDC / Kafka)
- Distributed search (OpenSearch)
- Partition pruning / compaction
- Multi-tenant isolation