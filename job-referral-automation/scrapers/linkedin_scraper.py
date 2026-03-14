import random
import time

from scrapers.base_scraper import BaseScraper
from config import LINKEDIN_SEARCH_URLS, JOBS_PER_SEARCH


class LinkedInScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.visited_jobs = set()

    # --------------------------------
    # Close popups
    # --------------------------------
    def close_popups(self):

        selectors = [
            "button[aria-label='Dismiss']",
            "button[aria-label='Close']",
            "button.artdeco-modal__dismiss",
            "button[aria-label='Sign in']",
            "button[data-control-name='dismiss']"
        ]

        for selector in selectors:
            try:
                btn = self.page.query_selector(selector)
                if btn:
                    btn.click()
                    print("Popup closed")
                    time.sleep(random.uniform(0.5, 1.5))
            except:
                pass

    # --------------------------------
    # Extract job cards (FAST)
    # --------------------------------
    def extract_job_cards(self):

        print("Extracting job cards...")

        jobs = []

        cards = self.page.query_selector_all("ul.jobs-search__results-list li")

        for card in cards:

            try:

                title_el = card.query_selector("h3")
                company_el = card.query_selector("h4")
                location_el = card.query_selector(".job-search-card__location")
                link_el = card.query_selector("a")

                if not link_el:
                    continue

                link = link_el.get_attribute("href")

                if not link or "/jobs/view/" not in link:
                    continue

                link = link.split("?")[0]

                if link in self.visited_jobs:
                    continue

                title = title_el.inner_text().strip() if title_el else "N/A"
                company = company_el.inner_text().strip() if company_el else "N/A"
                location = location_el.inner_text().strip() if location_el else "N/A"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "job_link": link
                })

            except:
                continue

        print("Job cards extracted:", len(jobs))

        return jobs

    # --------------------------------
    # Fetch extra details (optional)
    # --------------------------------
    def enrich_job(self, job):

        try:

            if not self.safe_goto(job["job_link"]):
                return job

            posted_el = self.page.query_selector("span.posted-time-ago__text")

            if posted_el:
                job["posted_time"] = posted_el.inner_text().strip()
            else:
                job["posted_time"] = "N/A"

        except:
            job["posted_time"] = "N/A"

        return job

    # --------------------------------
    # Main scraper
    # --------------------------------
    def scrape(self):

        print("Starting LinkedIn scraper")

        self.start_timer()
        self.start_browser()

        jobs_data = []

        try:

            for search in LINKEDIN_SEARCH_URLS:

                location = search["location"]
                level = search["level"]
                url = search["url"]

                print("\n================================")
                print("Scanning:", location, "|", level)
                print("================================")

                if not self.safe_goto(url):
                    continue

                self.close_popups()

                # Scroll to load jobs
                self.scroll_page(4)

                cards = self.extract_job_cards()

                cards = cards[:JOBS_PER_SEARCH]

                print("Processing jobs:", len(cards))

                for job in cards:

                    job = self.enrich_job(job)

                    job["platform"] = "LinkedIn"
                    job["search_location"] = location
                    job["search_level"] = level
                    job["seniority_level"] = level

                    jobs_data.append(job)

                    self.visited_jobs.add(job["job_link"])

                    time.sleep(random.uniform(0.8, 2))

        finally:

            self.close_browser()

        self.save_jobs_to_excel(jobs_data)

        self.stop_timer()

        execution_time = self.get_execution_time()

        print("\n================================")
        print("LinkedIn Scraper Finished")
        print("Total Execution Time:", execution_time)
        print("================================\n")

        return jobs_data, execution_time
