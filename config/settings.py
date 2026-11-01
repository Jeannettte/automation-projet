"""Environment configuration. Values come from environment variables / .env,
so no URL or timeout is hardcoded inside page objects or tests."""
import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://demoqa.com").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "false").strip().lower() == "true"
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

USENAME = os.getenv("USENAME", "test-api")
PASSWORD = os.getenv("PASSWORD", "Aa123###")
USERID = os.getenv("USERID", "bf9a0d32-0825-4cbd-8c74-4e8debce519f")


