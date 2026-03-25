import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.main import app
from app.db import get_conn


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def temp_dirs(tmp_path, monkeypatch):
    state_dir = tmp_path / "state"
    lake_dir = tmp_path / "lake"
    events_dir = tmp_path / "events"

    state_dir.mkdir(parents=True, exist_ok=True)
    lake_dir.mkdir(parents=True, exist_ok=True)
    events_dir.mkdir(parents=True, exist_ok=True)

    # checkpoint.py
    monkeypatch.setattr("app.checkpoint.CHECKPOINT_PATH", str(state_dir / "checkpoint.json"))

    # if your code uses hardcoded lake/event paths in other modules,
    # patch them there too if needed
    monkeypatch.setenv("STATE_DIR", str(state_dir))
    monkeypatch.setenv("LAKE_DIR", str(lake_dir))
    monkeypatch.setenv("EVENTS_DIR", str(events_dir))

    return {
        "state_dir": state_dir,
        "lake_dir": lake_dir,
        "events_dir": events_dir,
    }


@pytest.fixture
def reset_db():
    """
    Clears tables and reseeds deterministic test data.
    Assumes Postgres is already running and schema exists.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE cases RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE customers RESTART IDENTITY CASCADE;")

            # seed 3 customers
            cur.execute("""
                INSERT INTO customers (name, email, country, updated_at)
                VALUES
                  ('Alice', 'alice@example.com', 'US', '2026-03-01T00:00:00+00:00'),
                  ('Bob', 'bob@example.com', 'CA', '2026-03-02T00:00:00+00:00'),
                  ('Carol', 'carol@example.com', 'UK', '2026-03-03T00:00:00+00:00');
            """)

            # seed 5 cases
            cur.execute("""
                INSERT INTO cases (customer_id, title, description, status, updated_at)
                VALUES
                  (1, 'Billing discrepancy', 'billing reconciliation invoice mismatch', 'open', '2026-03-04T00:00:00+00:00'),
                  (1, 'Fraud review', 'fraud signal requires manual review', 'in_progress', '2026-03-05T00:00:00+00:00'),
                  (2, 'AML verification', 'aml compliance onboarding verification', 'open', '2026-03-06T00:00:00+00:00'),
                  (3, 'Payments delay', 'payments settlement delay investigation', 'closed', '2026-03-07T00:00:00+00:00'),
                  (2, 'Audit evidence', 'audit trail evidence collection needed', 'open', '2026-03-08T00:00:00+00:00');
            """)
        conn.commit()