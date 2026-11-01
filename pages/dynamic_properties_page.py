"""Page object for https://demoqa.com/dynamic-properties

"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DynamicPropertiesPage(BasePage):
    PATH = "/dynamic-properties"
    VISIBLE_AFTER_BUTTON = (By.ID, "visibleAfter")
    
    def wait_for_dynamic_button(self) -> bool:
        return self.is_displayed(self.VISIBLE_AFTER_BUTTON, timeout=6)

