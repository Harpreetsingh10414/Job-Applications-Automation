import psycopg2
from config import DATABASE_CONFIG


def get_connection():
    return psycopg2.connect(
        host=DATABASE_CONFIG["host"],
        database=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        port=DATABASE_CONFIG["port"]
    )


def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    cursor.close()
    conn.close()


def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result