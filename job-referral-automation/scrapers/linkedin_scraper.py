from scrapers.base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):

    def __init__(self):
        super().__init__()

    def close_popups(self):

        selectors = [
            "button[aria-label='Dismiss']",
            "button[aria-label='Close']",
            "button.artdeco-modal__dismiss"
        ]

        for selector in selectors:
            try:
                btn = self.page.query_selector(selector)
                if btn:
                    btn.click()
                    print("Popup closed")
                    self.random_delay()
            except:
                pass

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

                    links.add(clean_link)

            except:
                continue

        print("Total job links collected:", len(links))

        return list(links)

    def scrape_job_page(self, url):

        print("Opening job:", url)

        try:

            self.page.goto(url)

            self.random_delay()

            self.close_popups()

            # expand description
            try:
                show_more = self.page.query_selector(
                    "button.show-more-less-html__button"
                )
                if show_more:
                    show_more.click()
                    self.random_delay()
            except:
                pass

            # title
            title_el = self.page.query_selector("h1")

            title = title_el.inner_text().strip() if title_el else "N/A"

            # company
            company_el = self.page.query_selector(
                "a.topcard__org-name-link, span.topcard__flavor"
            )

            company = company_el.inner_text().strip() if company_el else "N/A"

            # location
            location_el = self.page.query_selector(
                "span.topcard__flavor--bullet"
            )

            location = location_el.inner_text().strip() if location_el else "N/A"

            # posted time
            posted_el = self.page.query_selector(
                "span.posted-time-ago__text"
            )

            posted_time = posted_el.inner_text().strip() if posted_el else "N/A"

            # seniority
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

            # description
            desc_el = self.page.query_selector(
                "div.show-more-less-html__markup"
            )

            description = desc_el.inner_text().strip() if desc_el else "N/A"

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "posted_time": posted_time,
                "seniority_level": seniority,
                "job_link": url,
                "description": description
            }

            print("-----")
            print("Title:", title)
            print("Company:", company)
            print("Location:", location)
            print("Posted:", posted_time)
            print("Seniority:", seniority)
            print("Description Length:", len(description))

            return job_data

        except Exception as e:

            print("Error scraping job:", e)

            return None

    def scrape(self):

        print("Starting LinkedIn scraper")

        self.start_browser()

        jobs_data = []

        try:

            url = "https://www.linkedin.com/jobs/search?keywords=Software%20%2B%20Java%20%2B%20Backend&location=India&geoId=102713980&f_JT=F&f_E=2%2C3%2C4&f_TPR=r86400&f_PP=104869687%2C106442238%2C105214831%2C105556991%2C103671728%2C106164952&position=1&pageNum=0"

            self.page.goto(url)

            self.random_delay()

            print("Page loaded")

            self.scroll_page(8)

            job_links = self.collect_job_links()

            for link in job_links[:5]:

                job_data = self.scrape_job_page(link)

                if job_data:
                    jobs_data.append(job_data)

                # human delay (important)
                self.random_delay()

        except Exception as e:

            print("Scraper error:", e)

        finally:

            self.close_browser()

        return jobs_data