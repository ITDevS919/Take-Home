import json
from pathlib import Path
from fastapi.testclient import TestClient

from app.checkpoint import load_checkpoint
from app.db import get_conn
from app.main import app


def test_ingest_checkpoint_and_idempotency(client, temp_dirs, reset_db, monkeypatch):
    lake_dir = temp_dirs["lake_dir"]
    checkpoint_path = Path(temp_dirs["state_dir"]) / "checkpoint.json"

    # Patch lake paths if your ingest.py hardcodes "./lake/..."
    def fake_run_paths(date_str):
        return (
            str(lake_dir / f"customers/date={date_str}/data.jsonl"),
            str(lake_dir / f"cases/date={date_str}/data.jsonl"),
        )

    # If your code does not expose a helper for paths, skip this patch.
    # Only keep it if you refactor path building into a helper.

    # 1) First ingest
    response = client.post("/ingest?dry_run=false")
    assert response.status_code == 200, response.text

    body = response.json()

    assert "checkpoint_before" in body
    assert "checkpoint_after" in body
    assert body["tables"]["customers"]["delta_row_count"] == 3
    assert body["tables"]["cases"]["delta_row_count"] == 5

    assert checkpoint_path.exists()

    with open(checkpoint_path, "r", encoding="utf-8") as f:
        checkpoint_data = json.load(f)

    first_checkpoint = checkpoint_data["watermark"]
    assert first_checkpoint == body["checkpoint_after"]

    # Check lake files exist
    customer_paths = body["tables"]["customers"]["lake_paths"]
    case_paths = body["tables"]["cases"]["lake_paths"]

    for p in customer_paths + case_paths:
        assert Path(p).exists(), f"Expected lake file missing: {p}"

    # 2) Second ingest without any DB changes
    response2 = client.post("/ingest?dry_run=false")
    assert response2.status_code == 200, response2.text

    body2 = response2.json()

    assert body2["tables"]["customers"]["delta_row_count"] == 0
    assert body2["tables"]["cases"]["delta_row_count"] == 0

    with open(checkpoint_path, "r", encoding="utf-8") as f:
        checkpoint_data2 = json.load(f)

    second_checkpoint = checkpoint_data2["watermark"]

    # checkpoint should remain unchanged on no-op run
    assert second_checkpoint == first_checkpoint
    assert body2["checkpoint_after"] == first_checkpoint


def test_ingest_dry_run_does_not_write_or_advance_checkpoint(client, temp_dirs, reset_db):
    checkpoint_path = Path(temp_dirs["state_dir"]) / "checkpoint.json"

    response = client.post("/ingest?dry_run=true")
    assert response.status_code == 200, response.text

    body = response.json()

    assert body["tables"]["customers"]["delta_row_count"] == 3
    assert body["tables"]["cases"]["delta_row_count"] == 5

    # dry run must not create checkpoint
    assert not checkpoint_path.exists()

    # dry run should not write files
    lake_files = list(Path(temp_dirs["lake_dir"]).rglob("*.jsonl"))
    assert lake_files == []


def test_ingest_failure_does_not_advance_checkpoint(temp_dirs, reset_db, monkeypatch):
    checkpoint_path = Path(temp_dirs["state_dir"]) / "checkpoint.json"

    def boom(*args, **kwargs):
        raise RuntimeError("simulated lake write failure")

    monkeypatch.setattr("app.ingest.write_jsonl_atomic", boom)

    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/ingest?dry_run=false")
    assert response.status_code == 500
    assert not checkpoint_path.exists()