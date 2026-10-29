"""Base class for all page objects: waits, safe clicks, typing helpers.

Rule: no time.sleep anywhere. Every interaction waits for a condition.
"""
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings

# DemoQA shows a fixed ad banner and a footer that can cover buttons.
_REMOVE_ADS_JS = """
for (const selector of ['#fixedban', 'footer', 'iframe[id^="google_ads"]']) {
    document.querySelectorAll(selector).forEach(el => el.remove());
}
"""


class BasePage:
    PATH = ""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.DEFAULT_TIMEOUT)

    def open(self):
        self.driver.get(f"{settings.BASE_URL}{self.PATH}")
        self.driver.execute_script(_REMOVE_ADS_JS)
        return self

    # --- finding -----------------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # --- actions -----------------------------------------------------------
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_into_view(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Something (ad, sticky bar) covers the element: click through JS.
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text, clear=True):
        element = self.find_visible(locator)
        self.scroll_into_view(element)
        if clear:
            element.clear()
        element.send_keys(text)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    # --- reading -----------------------------------------------------------
    def text_of(self, locator) -> str:
        return self.find_visible(locator).text.strip()

    def value_of(self, locator) -> str:
        return self.find(locator).get_attribute("value")

    def is_valid(self, locator) -> bool:
        """HTML5 constraint validation result (required, pattern, ...)."""
        return self.driver.execute_script(
            "return arguments[0].checkValidity();", self.find(locator)
        )

    def is_displayed(self, locator, timeout=settings.DEFAULT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False
