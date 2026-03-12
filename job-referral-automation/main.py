from database.db import get_connection
from scrapers.linkedin_scraper import LinkedInScraper

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

def test_scraper():
    scraper = LinkedInScraper()
    scraper.scrape()


if __name__ == "__main__":
    test_scraper()