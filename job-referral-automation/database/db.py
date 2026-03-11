import psycopg2
from config import DATABASE_CONFIG


def get_connection():
    conn = psycopg2.connect(
        host=DATABASE_CONFIG["host"],
        database=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        port=DATABASE_CONFIG["port"]
    )
    return conn