"""Environment configuration. Values come from environment variables / .env,
so no URL or timeout is hardcoded inside page objects or tests."""
import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://demoqa.com").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "false").strip().lower() == "true"
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
