from types import SimpleNamespace

import pytest

from app.config import Settings
from app.models import RecommendationRequest
from app.services.gemini_service import (
    GeminiBudgetService,
    GeminiGenerationError,
    GeminiNotConfiguredError,
)


VALID_OUTPUT = """{
  "summary": "A student-friendly celebration plan with a protected backup amount.",
  "items": [
    {"name": "Venue", "reason": "Affordable local hall", "weight": 25, "icon": "🏛️"},
    {"name": "Food", "reason": "Simple menu for guests", "weight": 40, "icon": "🍽️"},
    {"name": "Decor", "reason": "Reusable themed decoration", "weight": 20, "icon": "🎈"},
    {"name": "Photos", "reason": "Capture the important moments", "weight": 15, "icon": "📸"}
  ]
}"""


class FakeInteractions:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        if self.error:
            raise self.error
        return SimpleNamespace(output_text=self.output_text)


class FakeClient:
    def __init__(self, interactions):
        self.interactions = interactions


def test_valid_gemini_json_becomes_a_safe_plan():
    interactions = FakeInteractions(output_text=VALID_OUTPUT)
    service = GeminiBudgetService(
        Settings(gemini_api_key="test-key"),
        client=FakeClient(interactions),
    )
    request = RecommendationRequest(category="party", budget=30_000, preference="College Event")

    plan = service.generate(request)

    assert plan.source == "gemini"
    assert plan.model == "gemini-3.8-flash"
    assert plan.total + plan.remaining == 30_000
    assert interactions.last_kwargs["response_format"]["mime_type"] == "application/json"
    assert "schema" in interactions.last_kwargs["response_format"]
    assert "College Event" in interactions.last_kwargs["input"]


def test_gemini_failure_does_not_switch_to_a_demo_plan():
    service = GeminiBudgetService(
        Settings(gemini_api_key="test-key"),
        client=FakeClient(FakeInteractions(error=RuntimeError("network unavailable"))),
    )
    request = RecommendationRequest(category="home", budget=25_000, preference="Modern")
    with pytest.raises(GeminiGenerationError):
        service.generate(request)


def test_missing_key_requires_configuration():
    service = GeminiBudgetService(Settings(gemini_api_key=None))
    request = RecommendationRequest(category="jewellery", budget=40_000, preference="Daily Wear")
    with pytest.raises(GeminiNotConfiguredError):
        service.generate(request)


@pytest.mark.parametrize("output", ["", "not-json", '{"summary": "missing items"}'])
def test_invalid_gemini_output_is_rejected(output):
    service = GeminiBudgetService(
        Settings(gemini_api_key="test-key"),
        client=FakeClient(FakeInteractions(output_text=output)),
    )
    request = RecommendationRequest(category="home", budget=25_000, preference="Minimal")
    with pytest.raises(GeminiGenerationError):
        service.generate(request)
