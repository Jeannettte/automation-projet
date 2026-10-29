"""UI-01 .. UI-04: DemoQA Practice Form.

Each test opens its own page, uses its own unique data and depends on no other
test, so the whole file can run in parallel (pytest -n 4).
"""
import pytest

from pages.practice_form_page import PracticeFormPage
from utils.data_factory import build_student, load_json

CONFIRMATION_TITLE = "Thanks for submitting the form"
PHONE_CASES = load_json("phone_boundaries.json")


@pytest.fixture
def form(driver) -> PracticeFormPage:
    return PracticeFormPage(driver).open()


@pytest.mark.ui
def test_ui_01_valid_form_is_submitted_and_data_is_displayed(form):
    """UI-01 (positive): a fully valid form shows a confirmation with our data."""
    student = build_student()

    form.fill_all_fields(student)
    form.submit()

    assert form.is_confirmation_displayed(), "confirmation modal should appear"
    assert form.confirmation_title() == CONFIRMATION_TITLE
    values = form.submitted_values()
    assert values["Student Name"] == student.full_name
    assert values["Student Email"] == student.email
    assert values["Gender"] == student.gender
    assert values["Mobile"] == student.phone
    # Textarea is multi-line: both lines must be present in the confirmation.
    for line in student.address.splitlines():
        assert line in values["Address"]


@pytest.mark.ui
def test_ui_02_missing_required_fields_are_rejected(form):
    """UI-02 (negative / field validation): empty submit is blocked."""
    form.submit()

    assert form.form_was_validated(), "form should switch to validated state"
    assert not form.is_valid(form.FIRST_NAME), "first name is required"
    assert not form.is_valid(form.LAST_NAME), "last name is required"
    assert not form.is_valid(form.FIRST_GENDER_RADIO), "gender is required"
    assert not form.is_valid(form.PHONE), "mobile number is required"
    assert not form.is_confirmation_displayed(timeout=2), "nothing must be submitted"


@pytest.mark.ui
@pytest.mark.parametrize("case", PHONE_CASES, ids=[c["id"] for c in PHONE_CASES])
def test_ui_03_phone_boundaries_9_and_10_digits(form, case):
    """UI-03 (boundary, data-driven): 9 digits rejected, 10 digits accepted."""
    student = build_student(phone=case["phone"])

    form.fill_all_fields(student)
    form.submit()

    if case["accepted"]:
        assert form.is_confirmation_displayed(), case["case"]
        assert form.submitted_values()["Mobile"] == case["phone"]
    else:
        assert form.form_was_validated(), case["case"]
        assert not form.is_valid(form.PHONE), case["case"]
        assert not form.is_confirmation_displayed(timeout=2), case["case"]


@pytest.mark.ui
def test_ui_03c_phone_above_limit_never_accepts_more_than_10_digits(form):
    """UI-03c (boundary): 11 digits must never be accepted as-is.

    Depending on the app, the field either truncates the input to 10 digits or
    the form rejects it. Both are acceptable; storing 11 digits is not.
    """
    student = build_student(phone="06123456789")

    form.fill_all_fields(student)
    typed_value = form.phone_value()
    form.submit()

    if form.is_confirmation_displayed(timeout=3):
        assert len(form.submitted_values()["Mobile"]) <= 10
    else:
        assert len(typed_value) > 10, "rejected form implies the 11 digits were kept"
        assert not form.is_valid(form.PHONE)


@pytest.mark.ui
def test_ui_04_dropdowns_and_date_picker_selection_is_kept(form):
    """UI-04 (state verification): state/city and date are shown after submit."""
    student = build_student()

    form.fill_required_fields(student)
    form.pick_birth_date(year=1995, month_name="March", day=15)
    form.select_state("NCR")
    form.select_city("Delhi")

    # The widgets themselves display what we picked.
    assert form.birth_date_value() == "15 Mar 1995"
    assert form.selected_state() == "NCR"
    assert form.selected_city() == "Delhi"

    form.submit()

    assert form.is_confirmation_displayed()
    values = form.submitted_values()
    assert values["Date of Birth"] == "15 March,1995"
    assert values["State and City"] == "NCR Delhi"
