import json
import os

CHECKPOINT_PATH = "./state/checkpoint.json"
DEFAULT_WATERMARK = "1970-01-01T00:00:00+00:00"


def load_checkpoint() -> str:
    if not os.path.exists(CHECKPOINT_PATH):
        return DEFAULT_WATERMARK

    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("watermark", DEFAULT_WATERMARK)


def save_checkpoint_atomic(watermark: str):
    os.makedirs("./state", exist_ok=True)
    temp_path = CHECKPOINT_PATH + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump({"watermark": watermark}, f)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_path, CHECKPOINT_PATH)