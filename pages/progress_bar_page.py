"""Page object for https://demoqa.com/progress-bar

"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProgressBarPage(BasePage):
    PATH = "/progress-bar"
    START_STOP_BUTTON = (By.ID, "startStopButton")
    RESET_BUTTON = (By.ID, "resetButton") # The button start stop become reset when the progress bar is completed
    PROGRESS_BAR = (By.CSS_SELECTOR, ".progress-bar.bg-success") # become green at 100%
    
    def click_start(self):
        self.click(self.START_STOP_BUTTON)
        
    def wait_for_completion(self):
        # Wait for the progress bar to reach 100% (can take ~10 seconds)
        self.find_visible(self.PROGRESS_BAR)
        
    def get_button_text(self) -> str:
        if (self.find_visible(self.RESET_BUTTON)):
            return self.text_of(self.RESET_BUTTON)
        else:
            return self.text_of(self.START_STOP_BUTTON)

