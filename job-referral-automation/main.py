from database.db import get_connection
from scrapers.linkedin_scraper import LinkedInScraper

from utils.job_metadata import generate_job_metadata
from utils.email_sender import send_email_report

from config import EMAIL_CONFIG


def run():

    print("Starting Job Intelligence Automation")

    scraper = LinkedInScraper()

    jobs, execution_time = scraper.scrape()

    if not jobs:
        print("No jobs scraped. Email will not be sent.")
        return

    metadata = generate_job_metadata(jobs)

    metadata["execution_time"] = execution_time

    send_email_report(
        metadata,
        scraper.excel_file,
        EMAIL_CONFIG["sender_email"],
        EMAIL_CONFIG["app_password"],
        EMAIL_CONFIG["receiver_email"]
    )

    print("Automation completed successfully")


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

    run()