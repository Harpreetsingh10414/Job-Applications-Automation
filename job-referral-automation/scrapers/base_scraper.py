import random
import time
import os
from datetime import datetime

from playwright.sync_api import sync_playwright
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


class BaseScraper:

    def __init__(self, proxy=None):

        self.browser = None
        self.page = None
        self.playwright = None
        self.proxy = proxy

        # Excel setup
        today = datetime.now().strftime("%Y_%m_%d")

        os.makedirs("job_reports", exist_ok=True)

        self.excel_file = f"job_reports/jobs_{today}.xlsx"

    # --------------------------------
    # Random User Agents
    # --------------------------------
    def get_random_user_agent(self):

        user_agents = [

            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",

            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",

            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"

        ]

        return random.choice(user_agents)

    # --------------------------------
    # Random Viewport
    # --------------------------------
    def get_random_viewport(self):

        viewports = [

            {"width": 1280, "height": 720},
            {"width": 1366, "height": 768},
            {"width": 1440, "height": 900},
            {"width": 1536, "height": 864},
            {"width": 1600, "height": 900}

        ]

        return random.choice(viewports)

    # --------------------------------
    # Start Browser
    # --------------------------------
    def start_browser(self):

        print("Launching browser...")

        self.playwright = sync_playwright().start()

        launch_args = [

            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-sandbox",
            "--disable-dev-shm-usage"

        ]

        browser_args = {

            "channel": "chrome",
            "headless": False,
            "slow_mo": random.randint(20, 80),
            "args": launch_args

        }

        if self.proxy:
            browser_args["proxy"] = {"server": self.proxy}

        self.browser = self.playwright.chromium.launch(**browser_args)

        context = self.browser.new_context(

            user_agent=self.get_random_user_agent(),
            viewport=self.get_random_viewport(),
            locale="en-US",
            timezone_id="Asia/Kolkata"

        )

        context.add_init_script(
            """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        )

        self.page = context.new_page()

        print("Browser started")

    # --------------------------------
    # Safe Navigation
    # --------------------------------
    def safe_goto(self, url, retries=3):

        for attempt in range(retries):

            try:

                print("Navigating:", url)

                self.page.goto(url, timeout=60000)

                self.random_delay(2, 4)

                return True

            except Exception as e:

                print("Navigation failed:", e)

                if attempt < retries - 1:

                    print("Retrying navigation...")
                    self.random_delay(3, 6)

                else:

                    print("Max retries reached")

        return False

    # --------------------------------
    # Random Delay
    # --------------------------------
    def random_delay(self, min_s=2, max_s=5):

        delay = random.uniform(min_s, max_s)

        time.sleep(delay)

    # --------------------------------
    # Human Mouse Movement
    # --------------------------------
    def move_mouse_randomly(self):

        try:

            for _ in range(random.randint(2, 5)):

                x = random.randint(0, 1200)
                y = random.randint(0, 800)

                self.page.mouse.move(x, y)

                self.random_delay(0.3, 1.2)

        except:
            pass

    # --------------------------------
    # Human Scroll
    # --------------------------------
    def scroll_page(self, scroll_count=5):

        for i in range(scroll_count):

            scroll_value = random.randint(2000, 4500)

            print("Scrolling page:", i + 1)

            try:
                self.page.mouse.wheel(0, scroll_value)
            except:
                self.page.evaluate(f"window.scrollBy(0,{scroll_value})")

            self.random_delay(1.5, 3.5)

    # --------------------------------
    # Random Page Interaction
    # --------------------------------
    def random_page_interaction(self):

        try:

            self.move_mouse_randomly()

            if random.random() < 0.4:
                self.scroll_page(random.randint(1, 2))

        except:
            pass

    # --------------------------------
    # Save Jobs to Excel
    # --------------------------------
    def save_jobs_to_excel(self, jobs):

        if not jobs:
            print("No jobs to save")
            return

        location_order = [
            "Delhi",
            "Gurgaon",
            "Noida",
            "Bangalore",
            "Hyderabad",
            "Mumbai",
            "Pune"
        ]

        def location_sort(job):
            loc = job.get("search_location", "")
            try:
                return location_order.index(loc)
            except ValueError:
                return len(location_order)

        jobs = sorted(jobs, key=location_sort)

        headers = [
            "Platform",
            "Title",
            "Company",
            "Location",
            "Search Location",
            "Level",
            "Posted Time",
            "Job Link",
            "Scraped At"
        ]

        if not os.path.exists(self.excel_file):

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Jobs"

            sheet.append(headers)

        else:

            workbook = load_workbook(self.excel_file)
            sheet = workbook.active

        for job in jobs:

            link = job.get("job_link")

            sheet.append([

                job.get("platform", "LinkedIn"),
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("search_location"),
                job.get("search_level"),
                job.get("posted_time"),
                f'=HYPERLINK("{link}", "Open Job")',
                datetime.now().strftime("%Y-%m-%d %H:%M")

            ])

        # Header styling
        header_fill = PatternFill(start_color="4F81BD", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        for col in range(1, len(headers) + 1):

            cell = sheet.cell(row=1, column=col)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        # Auto column width
        for column_cells in sheet.columns:

            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            sheet.column_dimensions[get_column_letter(column_cells[0].column)].width = min(length + 5, 50)

        sheet.freeze_panes = "A2"

        table_ref = f"A1:{get_column_letter(len(headers))}{sheet.max_row}"

        table = Table(displayName="JobsTable", ref=table_ref)

        style = TableStyleInfo(
            name="TableStyleMedium9",
            showRowStripes=True,
            showColumnStripes=False
        )

        table.tableStyleInfo = style
        sheet.add_table(table)

        workbook.save(self.excel_file)

        print("Excel report generated:", self.excel_file)

    # --------------------------------
    # Close Browser
    # --------------------------------
    def close_browser(self):

        print("Closing browser...")

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        print("Browser closed")