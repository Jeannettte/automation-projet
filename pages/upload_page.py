"""Page object for https://demoqa.com/upload-download

"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class UploadPage(BasePage):
    PATH = "/upload-download"
    
    UPLOAD_INPUT = (By.ID, "uploadFile")
    UPLOADED_PATH_TEXT = (By.ID, "uploadedFilePath")
    
    def upload_file(self, file_path: str):
        self.find(self.UPLOAD_INPUT).send_keys(file_path)
        
    def get_uploaded_file_path(self) -> str:
        return self.text_of(self.UPLOADED_PATH_TEXT)