"""Shared fixtures: browser lifecycle and screenshot-on-failure evidence."""
import re
from pathlib import Path

import pytest
from selenium import webdriver

from config import settings

EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence" / "screenshots"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase result (setup/call/teardown) on the test item."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request):
    """A fresh Chrome per test: no shared state, safe for parallel runs."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    if settings.HEADLESS:
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    yield browser

    failed = getattr(getattr(request.node, "rep_call", None), "failed", False)
    if failed:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
        browser.save_screenshot(str(EVIDENCE_DIR / f"{safe_name}.png"))
    browser.quit()
