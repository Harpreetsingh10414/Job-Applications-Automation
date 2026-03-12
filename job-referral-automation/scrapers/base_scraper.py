from playwright.sync_api import sync_playwright
import time
import random


class BaseScraper:

    def __init__(self):
        self.browser = None
        self.page = None

    def start_browser(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def scroll_page(self, scroll_count=5):

        for i in range(scroll_count):

            print("Scrolling...", i + 1)

            self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")

            self.random_delay()

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.playwright.stop()

    def random_delay(self):
        time.sleep(random.uniform(2, 4))
