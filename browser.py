from playwright.sync_api import (

    sync_playwright
)

from config import (

    BROWSER_HEADLESS,

    DEBUG
)

# =========================================
# BROWSER CLASS
# =========================================

class BrowserController:

    def __init__(self):

        self.playwright = None

        self.browser = None

        self.page = None

    # =====================================
    # START
    # =====================================

    def start(self):

        if self.browser:

            return "Browser already started."

        self.playwright = (
            sync_playwright()
            .start()
        )

        self.browser = (
            self.playwright.chromium.launch(
                headless=BROWSER_HEADLESS
            )
        )

        self.page = (
            self.browser.new_page()
        )

        return "Browser started."

    # =====================================
    # OPEN URL
    # =====================================

    def open(
        self,
        url
    ):

        if not self.page:

            self.start()

        self.page.goto(url)

        return f"Opened {url}"

    # =====================================
    # SEARCH GOOGLE
    # =====================================

    def google(
        self,
        query
    ):

        if not self.page:

            self.start()

        url = (

            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        self.page.goto(url)

        return (
            f"Searched Google: {query}"
        )

    # =====================================
    # CLICK
    # =====================================

    def click(
        self,
        selector
    ):

        if not self.page:

            return "Browser not started."

        self.page.click(selector)

        return (
            f"Clicked {selector}"
        )

    # =====================================
    # TYPE
    # =====================================

    def type(
        self,
        selector,
        text
    ):

        if not self.page:

            return "Browser not started."

        self.page.fill(
            selector,
            text
        )

        return (
            f"Typed into {selector}"
        )

    # =====================================
    # HTML
    # =====================================

    def html(self):

        if not self.page:

            return "Browser not started."

        return self.page.content()

    # =====================================
    # TITLE
    # =====================================

    def title(self):

        if not self.page:

            return "Browser not started."

        return self.page.title()

    # =====================================
    # SCREENSHOT
    # =====================================

    def screenshot(
        self,
        path="browser.png"
    ):

        if not self.page:

            return "Browser not started."

        self.page.screenshot(
            path=path
        )

        return path

    # =====================================
    # CURRENT URL
    # =====================================

    def current_url(self):

        if not self.page:

            return "Browser not started."

        return self.page.url

    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        if self.browser:

            self.browser.close()

        if self.playwright:

            self.playwright.stop()

        self.browser = None

        self.page = None

        self.playwright = None

        return "Browser closed."

# =========================================
# GLOBAL INSTANCE
# =========================================

browser = BrowserController()