import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "interop",
    "user": "interop",
    "password": "interop",
}


def get_conn():
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


def fetch_customer_deltas(checkpoint: str):
    sql = """
        SELECT customer_id, name, email, country, updated_at
        FROM customers
        WHERE updated_at > %s
        ORDER BY updated_at, customer_id
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (checkpoint,))
            return cur.fetchall()


def fetch_case_deltas(checkpoint: str):
    sql = """
        SELECT case_id, customer_id, title, description, status, updated_at
        FROM cases
        WHERE updated_at > %s
        ORDER BY updated_at, case_id
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (checkpoint,))
            return cur.fetchall()


def fetch_all_cases():
    sql = """
        SELECT case_id, customer_id, title, description, status, updated_at
        FROM cases
        ORDER BY case_id
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()