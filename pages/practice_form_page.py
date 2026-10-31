"""Page object for https://demoqa.com/automation-practice-form

Locators prefer stable ids / `for` attributes. No layout-based XPath.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from utils.data_factory import Student

GENDER_INDEX = {"Male": 1, "Female": 2, "Other": 3}


class PracticeFormPage(BasePage):
    PATH = "/automation-practice-form"

    # Form fields
    FORM = (By.ID, "userForm")
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    PHONE = (By.ID, "userNumber")
    ADDRESS = (By.ID, "currentAddress")  # <textarea>
    SUBMIT = (By.ID, "submit")
    FIRST_GENDER_RADIO = (By.ID, "gender-radio-1")
    PICTURE_INPUT = (By.ID, "uploadPicture")

    # Date picker (react-datepicker)
    DOB_INPUT = (By.ID, "dateOfBirthInput")
    DOB_YEAR_SELECT = (By.CSS_SELECTOR, "select.react-datepicker__year-select")
    DOB_MONTH_SELECT = (By.CSS_SELECTOR, "select.react-datepicker__month-select")

    # State / City dropdowns (react-select)
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    STATE_VALUE = (By.CSS_SELECTOR, "#state [class*='singleValue']")
    CITY_VALUE = (By.CSS_SELECTOR, "#city [class*='singleValue']")

    # Confirmation modal
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    MODAL_ROWS = (By.CSS_SELECTOR, ".modal-body table tbody tr")

    # --- filling the form ---------------------------------------------------
    def fill_first_name(self, value):
        self.type(self.FIRST_NAME, value)

    def fill_last_name(self, value):
        self.type(self.LAST_NAME, value)

    def fill_email(self, value):
        self.type(self.EMAIL, value)

    def select_gender(self, gender: str):
        index = GENDER_INDEX[gender]
        self.click((By.CSS_SELECTOR, f"label[for='gender-radio-{index}']"))

    def fill_phone(self, value):
        self.type(self.PHONE, value)

    def fill_address(self, value):
        self.type(self.ADDRESS, value)

    def pick_birth_date(self, year: int, month_name: str, day: int):
        """Select a date through the calendar widget (month name in English)."""
        self.click(self.DOB_INPUT)
        Select(self.find_visible(self.DOB_YEAR_SELECT)).select_by_value(str(year))
        Select(self.find_visible(self.DOB_MONTH_SELECT)).select_by_visible_text(
            month_name
        )
        self.click(
            (
                By.CSS_SELECTOR,
                f".react-datepicker__day--{day:03d}"
                ":not(.react-datepicker__day--outside-month)",
            )
        )

    def upload_picture(self, file_path: str):
        self.find(self.PICTURE_INPUT).send_keys(file_path)

    def select_state(self, state: str):
        self._select_react_option(self.STATE, state)

    def select_city(self, city: str):
        self._select_react_option(self.CITY, city)

    def _select_react_option(self, dropdown_locator, option_text: str):
        """react-select: type to filter, wait for the option, confirm with Enter."""
        container = self.find(dropdown_locator)
        self.scroll_into_view(container)
        search = container.find_element(By.CSS_SELECTOR, "input")
        search.send_keys(option_text)
        self.find_visible(
            (
                By.XPATH,
                "//div[contains(@id,'-option-')"
                f" and normalize-space()='{option_text}']",
            )
        )
        search.send_keys(Keys.ENTER)

    def fill_required_fields(self, student: Student):
        self.fill_first_name(student.first_name)
        self.fill_last_name(student.last_name)
        self.select_gender(student.gender)
        self.fill_phone(student.phone)

    def fill_all_fields(self, student: Student):
        self.fill_required_fields(student)
        self.fill_email(student.email)
        self.fill_address(student.address)

    def submit(self):
        self.click(self.SUBMIT)

    # --- reading state ------------------------------------------------------
    def is_confirmation_displayed(self, timeout=None) -> bool:
        if timeout is None:
            return self.is_displayed(self.MODAL_TITLE)
        return self.is_displayed(self.MODAL_TITLE, timeout)

    def confirmation_title(self) -> str:
        return self.text_of(self.MODAL_TITLE)

    def submitted_values(self) -> dict:
        """Confirmation table as {label: value}, e.g. {'Student Name': '...'}."""
        self.find_visible(self.MODAL_TITLE)
        values = {}
        for row in self.driver.find_elements(*self.MODAL_ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                values[cells[0].text.strip()] = cells[1].text.strip()
        return values

    def form_was_validated(self) -> bool:
        return "was-validated" in (self.find(self.FORM).get_attribute("class") or "")

    def phone_value(self) -> str:
        return self.value_of(self.PHONE)

    def birth_date_value(self) -> str:
        return self.value_of(self.DOB_INPUT)

    def selected_state(self) -> str:
        return self.text_of(self.STATE_VALUE)

    def selected_city(self) -> str:
        return self.text_of(self.CITY_VALUE)