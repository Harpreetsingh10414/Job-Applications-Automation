import random

from scrapers.base_scraper import BaseScraper
from config import LINKEDIN_SEARCH_URLS, JOBS_PER_SEARCH


class LinkedInScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.visited_jobs = set()

    # --------------------------------
    # Close LinkedIn Popups
    # --------------------------------
    def close_popups(self):

        selectors = [

            "button[aria-label='Dismiss']",
            "button[aria-label='Close']",
            "button.artdeco-modal__dismiss",
            "button[aria-label='Sign in']",
            "button[data-control-name='dismiss']",
            "button[aria-label='Reject cookies']"

        ]

        for selector in selectors:

            try:

                btn = self.page.query_selector(selector)

                if btn:

                    btn.click()

                    print("Popup closed")

                    self.random_delay(1, 2)

            except:
                pass

    # --------------------------------
    # Collect Job Links
    # --------------------------------
    def collect_job_links(self):

        print("Collecting job links...")

        links = set()

        job_cards = self.page.query_selector_all(
            "ul.jobs-search__results-list li a"
        )

        for card in job_cards:

            try:

                link = card.get_attribute("href")

                if link and "/jobs/view/" in link:

                    clean_link = link.split("?")[0]

                    if clean_link not in self.visited_jobs:
                        links.add(clean_link)

            except:
                continue

        print("Unique job links collected:", len(links))

        return list(links)

    # --------------------------------
    # Scrape Job Page
    # --------------------------------
    def scrape_job_page(self, url):

        print("Opening job:", url)

        try:

            if not self.safe_goto(url):
                return None

            self.close_popups()

            self.random_page_interaction()

            # Expand description
            try:

                show_more = self.page.query_selector(
                    "button.show-more-less-html__button"
                )

                if show_more:
                    show_more.click()
                    self.random_delay(1, 2)

            except:
                pass

            # ----------------
            # Title
            # ----------------
            title_el = self.page.query_selector("h1")
            title = title_el.inner_text().strip() if title_el else "N/A"

            # ----------------
            # Company
            # ----------------
            company_el = self.page.query_selector(
                "a.topcard__org-name-link, span.topcard__flavor"
            )

            company = company_el.inner_text().strip() if company_el else "N/A"

            # ----------------
            # Location
            # ----------------
            location_el = self.page.query_selector(
                "span.topcard__flavor--bullet"
            )

            location = location_el.inner_text().strip() if location_el else "N/A"

            # ----------------
            # Posted Time
            # ----------------
            posted_el = self.page.query_selector(
                "span.posted-time-ago__text"
            )

            posted_time = posted_el.inner_text().strip() if posted_el else "N/A"

            # ----------------
            # Seniority
            # ----------------
            seniority = "N/A"

            criteria = self.page.query_selector_all(
                "li.description__job-criteria-item"
            )

            for item in criteria:

                label = item.query_selector(
                    "h3.description__job-criteria-subheader"
                )

                value = item.query_selector(
                    "span.description__job-criteria-text"
                )

                if label and value:

                    if "Seniority level" in label.inner_text():

                        seniority = value.inner_text().strip()

            # ----------------
            # Description
            # ----------------
            desc_el = self.page.query_selector(
                "div.show-more-less-html__markup"
            )

            description = desc_el.inner_text().strip() if desc_el else "N/A"

            job_data = {

                "platform": "LinkedIn",

                "title": title,
                "company": company,
                "location": location,
                "posted_time": posted_time,
                "seniority_level": seniority,
                "job_link": url,
                "description": description

            }

            self.visited_jobs.add(url)

            return job_data

        except Exception as e:

            print("Error scraping job:", e)

            return None

    # --------------------------------
    # Main Scraper
    # --------------------------------
    def scrape(self):

        print("Starting LinkedIn scraper")

        self.start_browser()

        jobs_data = []

        try:

            for search in LINKEDIN_SEARCH_URLS:

                location = search["location"]
                level = search["level"]
                url = search["url"]

                print("\n================================")
                print("Scanning Location:", location)
                print("Experience Level:", level)
                print("================================\n")

                if not self.safe_goto(url):
                    continue

                # Close popups immediately
                self.close_popups()

                # Simulate human behaviour
                self.random_page_interaction()

                # Scroll to load jobs
                self.scroll_page(10)

                # Close popups again
                self.close_popups()

                job_links = self.collect_job_links()

                job_links = job_links[:JOBS_PER_SEARCH]

                print("Jobs to scrape:", len(job_links))

                for link in job_links:

                    if link in self.visited_jobs:
                        continue

                    job_data = self.scrape_job_page(link)

                    if job_data:

                        job_data["search_location"] = location
                        job_data["search_level"] = level

                        jobs_data.append(job_data)

                    self.random_delay(3, 7)

        except Exception as e:

            print("Scraper error:", e)

        finally:

            self.close_browser()

        # Save results to Excel
        self.save_jobs_to_excel(jobs_data)

        return jobs_data