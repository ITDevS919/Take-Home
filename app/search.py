import math
import re
import hashlib
from app.db import fetch_all_cases

CASE_INDEX = {}
VECTOR_SIZE = 128


def tokenize(text: str):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def token_to_bucket(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(digest, 16) % VECTOR_SIZE


def vectorize(text: str):
    vec = [0] * VECTOR_SIZE
    for token in tokenize(text):
        bucket = token_to_bucket(token)
        vec[bucket] += 1
    return vec


def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def initialize_search_index():
    global CASE_INDEX
    CASE_INDEX = {}

    rows = fetch_all_cases()
    for row in rows:
        text = f"{row['title']} {row['description']}"
        CASE_INDEX[row["case_id"]] = {
            "title": row["title"],
            "status": row["status"],
            "vector": vectorize(text),
        }


def search_cases(query: str, top_k: int = 5):
    query_vec = vectorize(query)
    results = []

    for case_id, payload in CASE_INDEX.items():
        score = cosine_similarity(query_vec, payload["vector"])
        results.append({
            "case_id": case_id,
            "score": score,
            "title": payload["title"],
            "status": payload["status"],
        })

    results.sort(key=lambda x: (-x["score"], x["case_id"]))
    return results[:top_k]