from database.db import get_connection


def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        print("Connected to PostgreSQL!")
        print("PostgreSQL version:", db_version)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Database connection failed:", e)


if __name__ == "__main__":
    test_connection()