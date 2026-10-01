import pytest
from fastapi.testclient import TestClient

from app.main import app, get_recommendation_service
from app.models import GeminiDraft
from app.services.budget_engine import build_plan
from app.services.gemini_service import GeminiGenerationError, GeminiNotConfiguredError


VALID_DRAFT = GeminiDraft.model_validate(
    {
        "summary": "A practical Gemini plan with a protected reserve for changing prices.",
        "items": [
            {"name": "Priority item", "reason": "Covers the main requirement", "weight": 40},
            {"name": "Supporting item", "reason": "Completes the selected plan", "weight": 25},
            {"name": "Quality check", "reason": "Protects the final purchase", "weight": 20},
            {"name": "Finishing", "reason": "Handles final adjustments", "weight": 15},
        ],
    }
)


class StubRecommendationService:
    def generate(self, request):
        return build_plan(request, VALID_DRAFT, model="gemini-test")


@pytest.fixture(autouse=True)
def mocked_gemini_service():
    app.dependency_overrides[get_recommendation_service] = lambda: StubRecommendationService()
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_home_page_loads_tharun_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "PocketSmart AI" in response.text
    assert "THARUN" in response.text


def test_frontend_calls_the_backend_and_has_no_demo_engine():
    response = client.get("/")
    assert 'fetch(`${API_BASE_URL}/api/recommendations`' in response.text
    assert "SMART DEMO MODE" not in response.text
    assert "smart_fallback" not in response.text


def test_frontend_has_no_login_or_create_account_flow():
    response = client.get("/")
    lowered = response.text.lower()
    assert "type=\"password\"" not in lowered
    assert "create account" not in lowered
    assert ">login<" not in lowered


def test_health_endpoint_does_not_expose_a_secret():
    response = client.get("/api/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["mode"] in {"gemini-ready", "gemini-key-required"}
    assert "api_key" not in data


def test_categories_endpoint():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {"home", "party", "jewellery"}


def test_recommendation_endpoint_returns_gemini_plan():
    response = client.post(
        "/api/recommendations",
        json={
            "category": "party",
            "budget": 30_000,
            "preference": "College Event",
            "notes": "100 guests and strong photo coverage",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["source"] == "gemini"
    assert data["model"] == "gemini-test"
    assert data["preference"] == "College Event"
    assert data["total"] + data["remaining"] == data["budget"]
    assert len(data["items"]) == 4


@pytest.mark.parametrize(
    "payload",
    [
        {"category": "home", "budget": 4_999, "preference": "Modern"},
        {"category": "travel", "budget": 25_000, "preference": "Modern"},
        {"category": "home", "budget": 10_000_001, "preference": "Modern"},
        {"category": "home", "budget": 25_000, "preference": ""},
        {"category": "party", "budget": 25_000, "preference": "Birthday", "notes": "x" * 501},
    ],
)
def test_invalid_input_returns_422(payload):
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422


def test_missing_key_is_reported_as_503():
    class MissingKeyService:
        def generate(self, request):
            raise GeminiNotConfiguredError("Gemini API key is not configured.")

    app.dependency_overrides[get_recommendation_service] = lambda: MissingKeyService()
    response = client.post(
        "/api/recommendations",
        json={"category": "home", "budget": 25_000, "preference": "Modern"},
    )
    assert response.status_code == 503
    assert "Gemini API key" in response.json()["detail"]


def test_gemini_failure_is_reported_as_502():
    class FailedGeminiService:
        def generate(self, request):
            raise GeminiGenerationError("Gemini could not generate a valid plan right now.")

    app.dependency_overrides[get_recommendation_service] = lambda: FailedGeminiService()
    response = client.post(
        "/api/recommendations",
        json={"category": "jewellery", "budget": 50_000, "preference": "Daily Wear"},
    )
    assert response.status_code == 502
    assert "Gemini" in response.json()["detail"]
