"""Test-data builders.

Every call generates unique values (random suffix), so tests never share data
and can safely run in parallel (pytest -n 4).
"""
import json
from dataclasses import dataclass, replace
from pathlib import Path
from uuid import uuid4

TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "test-data"


@dataclass(frozen=True)
class Student:
    first_name: str
    last_name: str
    email: str
    gender: str
    phone: str
    address: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def build_student(**overrides) -> Student:
    """Return a valid student with unique name/email. Override any field."""
    suffix = uuid4().hex[:6]
    student = Student(
        first_name="Alice",
        last_name=f"Martin{suffix}",
        email=f"alice.{suffix}@example.com",
        gender="Female",
        phone="0612345678",
        address=f"12 rue des Tests\nLille {suffix}",
    )
    return replace(student, **overrides)


def load_json(filename: str):
    with open(TEST_DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)
