# UI & API Test Automation – Selenium

Application under test: **DemoQA** – https://demoqa.com.

**Why Selenium, Python and pytest**
Selenium drives a real Chrome browser through the WebDriver protocol: it opens pages, fills fields, clicks, and reads what is displayed. It was the tool assigned to our team.

Python was chosen for its short, readable syntax and for its ecosystem, which covers every requirement of the assignment without extra tooling: pytest (test runner and assertions), pytest.mark.parametrize (data-driven tests), pytest-xdist (parallel execution), pytest-html (reports), requests and jsonschema (API tests), python-dotenv (configuration).

pytest fixtures give every test its own browser and handle setup/teardown, so tests stay short and focused on the scenario
### Application under test 
DemoQA (https://demoqa.com) is a public site built for practising test automation. Its Practice Form provides real behaviour for most mandatory controls: text fields, a phone number field, a multi-line textarea, radio buttons, a calendar date picker, dependent State/City dropdowns, and a confirmation dialog that displays the submitted data. The site is intended for practice, so automating it is consistent with its purpose (the team should still check its terms of use before submission).
BookStore API (DemoQA) exposes a REST API with account creation, token authentication and book operations, which allows status code, body, schema, authentication, CRUD and negative tests on a related and legitimately testable service.

### Project layout and responsabilities 
* config/settngs.py : reads BASE_URL, HEADLESS and DEFAULT_TIMEOUT from .env; nothing environment-specific is hardcoded.
* conftest.py : Provides the driver fixture (one fresh Chrome per test) and saves a screenshot to evidence/screenshots/ when a test fails.
* pages/base_page.py: Shared actions (find, click, type, read, wait) used by every page object.
* pages/practice_form_page.py: Everything about the Practice Form: locators, actions, and ways to read the page state.
* tests/ui/: 	Test scenarios and assertions only.
* test-data/ :Data sets for data-driven tests (JSON).
* utils/data_factory.py : Builds valid test data with unique values for each test.

### Page Object Model 
Each page has one class that owns its locators and actions. Tests call readable methods (fill_all_fields, submit, submitted_values) instead of touching the browser directly. If the application changes a locator, only the page object changes and the tests stay the same. All pages inherit from BasePage, which avoids duplicated waiting and clicking code (DRY).

### Locator strategy 
Locators prefer stable attributes: element ids (firstName, userNumber), for attributes of labels, and semantic CSS classes of widgets. We avoid XPath tied to page layout or position. The only XPath used targets dropdown options by their visible text, which is the stable part of that widget.

### Synchronization
No fixed sleep is used anywhere. BasePage relies on WebDriverWait with explicit conditions (presence, visibility, clickability) and a configurable timeout. Elements are scrolled into view before interaction. If a normal click is intercepted by an overlay (advertisement), the page object falls back to a JavaScript click, and the advertisement banner and footer are removed after page load. For the React-based State/City dropdowns, the page object types into the dropdown's search field, waits for the option to appear, and confirms with Enter; a plain click does not open this widget reliably.

### Assertions 
Tests check behaviour, not just that a click worked:

* the confirmation title and every displayed value 
* the HTML5 validity state of required fields (checkValidity), plus the "validated" state of the form, to confirm that invalid submissions are rejected;
* the absence of the confirmation dialog when a submission must be refused.

### Test data and data-driven testing
data_factory.py generates a valid student with a random suffix in the name and e-mail, so each test uses its own data. UI-10 is the main data-driven scenario: the same test function runs against the five entries of test-data/ui_10_form_cases.json. It covers two accepted submissions and three rejected submissions (missing first name, invalid email, and missing phone), and the report shows one result per data set. UI-03 separately uses test-data/phone_boundaries.json for the 9/10-digit boundary. UI-03c checks the upper boundary (11 digits) as a rule: the application must never accept more than 10 digits, whether it truncates the input or rejects the form.

Run UI-10 alone and generate the configured HTML report:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_ui_10_data_driven.py -v
```

Run the UI suite with four independent workers:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/ -m ui -n 4 -v
```

### Independence and parallel execution
* The driver fixture is function-scoped: every test starts its own browser.
* Each test opens its page and builds its own unique data; no test relies on another test, on a fixed record, or on shared state.
* The Practice Form does not persist data on the server, so parallel runs cannot conflict.

### Failure evidence and investigation
A failing UI test saves a screenshot in evidence/screenshots/ and the HTML report in reports/report.html. During development, UI-04 failed with a TimeoutException while selecting the State option: the option never became clickable. Our analysis is that the dropdown did not open when the helper clicked it (this widget reacts to real mouse events, and the helper's fallback JavaScript click does not trigger them). The cause was therefore the way the test interacted with the widget, not an application defect. The fix was to type in the dropdown's search field instead of clicking; the test then passed and the expected results were left unchanged.

### Test IDs

Each test function includes its ID in the name and docstring (for example test_ui_01_..., "UI-01"). The full inventory with descriptions, expected results and execution status is in Inventaire_des_tests.xlsx.