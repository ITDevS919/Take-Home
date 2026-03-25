from datetime import datetime, timezone
from uuid import uuid4

from app.checkpoint import load_checkpoint, save_checkpoint_atomic
from app.db import fetch_customer_deltas, fetch_case_deltas
from app.events import emit_event
from app.lake import write_jsonl_atomic
from app.search import initialize_search_index
from app.utils import utc_now_iso, schema_fingerprint


def _max_watermark(checkpoint_before, customer_rows, case_rows):
    timestamps = []

    for row in customer_rows:
        timestamps.append(row["updated_at"])
    for row in case_rows:
        timestamps.append(row["updated_at"])

    if not timestamps:
        return checkpoint_before

    max_ts = max(timestamps)
    return max_ts.isoformat() if hasattr(max_ts, "isoformat") else str(max_ts)


def run_ingest(dry_run: bool = True):
    run_id = str(uuid4())
    started_at = utc_now_iso()

    checkpoint_before = load_checkpoint()

    customer_rows = fetch_customer_deltas(checkpoint_before)
    case_rows = fetch_case_deltas(checkpoint_before)

    checkpoint_after = _max_watermark(checkpoint_before, customer_rows, case_rows)
    date_str = datetime.now(timezone.utc).date().isoformat()

    customer_path = f"./lake/customers/date={date_str}/data.jsonl"
    case_path = f"./lake/cases/date={date_str}/data.jsonl"

    customer_schema = schema_fingerprint([
        ("customer_id", "BIGINT"),
        ("name", "TEXT"),
        ("email", "TEXT"),
        ("country", "TEXT"),
        ("updated_at", "TIMESTAMPTZ"),
    ])

    case_schema = schema_fingerprint([
        ("case_id", "BIGINT"),
        ("customer_id", "BIGINT"),
        ("title", "TEXT"),
        ("description", "TEXT"),
        ("status", "TEXT"),
        ("updated_at", "TIMESTAMPTZ"),
    ])

    manifest = {
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": utc_now_iso(),
        "tables": {
            "customers": {
                "delta_row_count": len(customer_rows),
                "lake_paths": [customer_path],
                "schema_fingerprint": customer_schema,
            },
            "cases": {
                "delta_row_count": len(case_rows),
                "lake_paths": [case_path],
                "schema_fingerprint": case_schema,
            },
        },
        "checkpoint_before": checkpoint_before,
        "checkpoint_after": checkpoint_after,
    }

    if dry_run:
        return manifest

    if customer_rows:
        write_jsonl_atomic(customer_path, customer_rows)
    if case_rows:
        write_jsonl_atomic(case_path, case_rows)

    emit_event({
        "table": "customers",
        "run_id": run_id,
        "schema_fingerprint": customer_schema,
        "delta_row_count": len(customer_rows),
        "lake_paths": [customer_path],
        "checkpoint_after": checkpoint_after,
    })

    emit_event({
        "table": "cases",
        "run_id": run_id,
        "schema_fingerprint": case_schema,
        "delta_row_count": len(case_rows),
        "lake_paths": [case_path],
        "checkpoint_after": checkpoint_after,
    })

    initialize_search_index()
    save_checkpoint_atomic(checkpoint_after)

    return manifest