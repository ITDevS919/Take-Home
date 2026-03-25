import json
import os


def write_jsonl_atomic(path: str, rows: list[dict]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        for row in rows:
            serializable_row = {
                k: (v.isoformat() if hasattr(v, "isoformat") else v)
                for k, v in row.items()
            }
            f.write(json.dumps(serializable_row) + "\n")
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_path, path)