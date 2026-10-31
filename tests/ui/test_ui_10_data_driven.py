"""UI-10: data-driven validation of the DemoQA Practice Form."""
import pytest

from pages.practice_form_page import PracticeFormPage
from utils.data_factory import build_student, load_json

CASES = load_json("ui_10_form_cases.json")
CONFIRMATION_TITLE = "Thanks for submitting the form"

FIELD_LOCATORS = {
    "first_name": PracticeFormPage.FIRST_NAME,
    "email": PracticeFormPage.EMAIL,
    "phone": PracticeFormPage.PHONE,
}


@pytest.fixture
def form(driver) -> PracticeFormPage:
    return PracticeFormPage(driver).open()


@pytest.mark.ui
@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_ui_10_data_driven_form_validation(form, case):
    """UI-10: run the same form workflow against multiple JSON data sets."""
    student = build_student(**case["overrides"])

    form.fill_available_fields(student)
    form.submit()

    if case["accepted"]:
        assert form.is_confirmation_displayed(), case["description"]
        assert form.confirmation_title() == CONFIRMATION_TITLE
        values = form.submitted_values()
        assert values["Student Name"] == student.full_name
        assert values["Student Email"] == student.email
        assert values["Gender"] == student.gender
        assert values["Mobile"] == student.phone
    else:
        invalid_locator = FIELD_LOCATORS[case["invalid_field"]]
        assert form.form_was_validated(), case["description"]
        assert not form.is_valid(invalid_locator), case["description"]
        assert not form.is_confirmation_displayed(timeout=2), case["description"]
