import hashlib
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def schema_fingerprint(columns: list[tuple[str, str]]) -> str:
    raw = "|".join(f"{name}:{dtype}" for name, dtype in columns)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()