# UI & API Test Automation – Selenium (Python + pytest)

Application under test: **DemoQA** – https://demoqa.com (Practice Form, API: BookStore).

## Prerequisites
- Python 3.10+
- Google Chrome (Selenium 4 downloads the matching driver automatically)
- Git

## Installation
```bash
git clone <repository-url>
cd automation-project
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
```

## Configuration (`.env`)
| Variable | Default | Meaning |
|---|---|---|
| `BASE_URL` | `https://demoqa.com` | Application under test |
| `HEADLESS` | `false` | `true` runs Chrome without a window |
| `DEFAULT_TIMEOUT` | `10` | Explicit-wait timeout in seconds |

No secrets are stored in source code. Credentials (API tests) go in `.env`, which is git-ignored.

## Running the tests
```bash
pytest                          # whole suite, sequential
pytest -m smoke                 # quick sanity check
pytest tests/ui                 # UI tests only
pytest -k ui_03                 # one test / one data-driven test
pytest -n 4                     # parallel run on 4 workers (pytest-xdist)
HEADLESS=true pytest -n 4       # parallel + headless (Windows PowerShell: $env:HEADLESS="true"; pytest -n 4)
```

## Reports and evidence
- HTML report: `reports/report.html` (generated on every run; data-driven iterations appear as separate rows).
- Screenshots of failed UI tests: `evidence/screenshots/`.

## Project structure
```
config/        environment settings (read from .env)
pages/         page objects (BasePage + one class per page)
tests/ui/      UI tests
test-data/     JSON data sets for data-driven tests
utils/         test-data factory (unique data per test)
conftest.py    browser fixture, screenshot on failure
```

## Design decisions
- **Page Object Model**: tests contain scenarios and assertions only; locators and UI actions live in `pages/`. If the UI changes, only the page object changes.
- **Locators**: ids and `for` attributes first; no layout-based XPath.
- **Synchronization**: explicit waits (`WebDriverWait`) in `BasePage`; no `time.sleep`.
- **Independence / parallel**: one fresh browser per test, unique data per test (`utils/data_factory.py`), no shared state, no test relies on another.
- **Data-driven**: `pytest.mark.parametrize` fed by JSON files in `test-data/`.
