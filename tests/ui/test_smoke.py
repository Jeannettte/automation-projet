import pytest
from selenium.webdriver.common.by import By

from pages.practice_form_page import PracticeFormPage


@pytest.mark.ui
@pytest.mark.smoke
def test_practice_form_page_loads(driver):
    """Environment check: browser starts and the target page is reachable."""
    page = PracticeFormPage(driver).open()

    assert driver.find_element(By.TAG_NAME, "h1").text == "Practice Form"
    assert page.find_visible(page.SUBMIT).is_displayed()
