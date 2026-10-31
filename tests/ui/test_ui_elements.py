"""UI-05 .. UI-09: DemoQA upload, alert and dynamic element tests.

"""
import pytest
from pathlib import Path
from pages.practice_form_page import PracticeFormPage
from pages.upload_page import UploadPage
from pages.alerts_page import AlertsPage
from pages.dynamic_properties_page import DynamicPropertiesPage
from pages.progress_bar_page import ProgressBarPage
from utils.data_factory import build_student


TEST_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test-data"

@pytest.mark.ui
def test_ui_05_upload_image_in_form(driver):
    """UI-05 : Upload a picture in the form and verify the state after submission."""
    form = PracticeFormPage(driver).open()
    student = build_student()
    
    # Fill the required fields to be able to submit
    form.fill_required_fields(student)
    
    # Upload of the image
    image_path = str(TEST_DATA_DIR / "test_image.png")
    form.upload_picture(image_path)
    
    form.submit()
    assert form.is_confirmation_displayed()
    
    # Verification that the image is properly saved in the confirmation modal
    values = form.submitted_values()
    assert "test_image.png" in values.get("Picture", ""), "The image name should appear in the confirmation"

@pytest.mark.ui
def test_ui_06_upload_standard_file(driver):
    """UI-06 : Upload a standard text file and verify the displayed path."""
    page = UploadPage(driver).open()
    
    file_path = str(TEST_DATA_DIR / "test_doc.txt")
    page.upload_file(file_path)
    
    result = page.get_uploaded_file_path()
    assert "test_doc.txt" in result, f"The expected text is not in the path: {result}"

@pytest.mark.ui
def test_ui_07_dialogue_confirm_cancel(driver):
    """UI-07 : Manage a dialog (Accept / Cancel) and verify the UI result."""
    page = AlertsPage(driver).open()
    
    # Test Accept
    page.trigger_confirm_alert()
    page.accept_alert()
    assert "Ok" in page.get_confirm_result()
    
    # Test Cancel
    page.trigger_confirm_alert()
    page.dismiss_alert()
    assert "Cancel" in page.get_confirm_result()

@pytest.mark.ui
def test_ui_08_dynamic_element_appears(driver):
    """UI-08 : Verify the appearance of a dynamic element without using sleep."""
    page = DynamicPropertiesPage(driver).open()
    
    # Wait dynamically for the element to appear (up to 6 seconds)
    is_visible = page.wait_for_dynamic_button()
    assert is_visible is True, "The dynamic button did not appear in time"

@pytest.mark.ui
def test_ui_09_progress_bar_state(driver):
    """UI-09 : Verify the state of an element (button) after submission / progress."""
    page = ProgressBarPage(driver).open()
    
    page.click_start()
    page.wait_for_completion()  # Wait for the progress bar to reach 100% (class bg-success)
    
    # After the progress bar reaches 100%, the "Start/Stop" button becomes "Reset"
    assert page.get_button_text() == "Reset", "The button should propose a Reset after completion"

