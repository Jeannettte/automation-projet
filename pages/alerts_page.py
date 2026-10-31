"""Page object for https://demoqa.com/alerts

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class AlertsPage(BasePage):
    PATH = "/alerts"
    
    CONFIRM_BUTTON = (By.ID, "confirmButton")
    CONFIRM_RESULT = (By.ID, "confirmResult")
    
    def trigger_confirm_alert(self):
        self.click(self.CONFIRM_BUTTON)
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        
    def accept_alert(self):
        self.driver.switch_to.alert.accept()
        
    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()
        
    def get_confirm_result(self) -> str:
        return self.text_of(self.CONFIRM_RESULT)