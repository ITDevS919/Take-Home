from app.search import initialize_search_index


def test_search_is_deterministic(client, temp_dirs, reset_db):
    # build index from seeded DB
    initialize_search_index()

    payload = {
        "query": "billing compliance reconciliation",
        "top_k": 3
    }

    response1 = client.post("/search", json=payload)
    response2 = client.post("/search", json=payload)

    assert response1.status_code == 200, response1.text
    assert response2.status_code == 200, response2.text

    results1 = response1.json()
    results2 = response2.json()

    assert results1 == results2
    assert len(results1) == 3

    # optional structural checks
    for row in results1:
        assert "case_id" in row
        assert "score" in row
        assert "title" in row
        assert "status" in row


def test_search_reflects_newly_ingested_data(client, temp_dirs, reset_db):
    # Initial ingest
    ingest_response = client.post("/ingest?dry_run=false")
    assert ingest_response.status_code == 200, ingest_response.text

    # Add a new highly relevant case directly into DB
    from app.db import get_conn
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cases (customer_id, title, description, status, updated_at)
                VALUES (
                    1,
                    'Compliance escalation',
                    'compliance aml fraud billing reconciliation urgent escalation',
                    'open',
                    '2026-03-20T00:00:00+00:00'
                );
            """)
        conn.commit()

    # Re-ingest so search index refreshes
    ingest_response2 = client.post("/ingest?dry_run=false")
    assert ingest_response2.status_code == 200, ingest_response2.text

    response = client.post("/search", json={
        "query": "aml fraud compliance billing reconciliation",
        "top_k": 5
    })

    assert response.status_code == 200, response.text
    results = response.json()

    assert len(results) > 0

    titles = [r["title"] for r in results]
    assert "Compliance escalation" in titles