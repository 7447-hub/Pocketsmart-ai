import pytest
from pydantic import ValidationError

from app.models import Category, GeminiDraft, RecommendationRequest
from app.services.budget_engine import build_plan


@pytest.fixture
def gemini_draft():
    return GeminiDraft.model_validate(
        {
            "summary": "A useful plan that protects ten percent for price changes.",
            "items": [
                {"name": "Main item", "reason": "Highest priority", "weight": 45},
                {"name": "Support item", "reason": "Supports the goal", "weight": 25},
                {"name": "Setup", "reason": "Covers practical setup", "weight": 20},
                {"name": "Finishing", "reason": "Completes the plan", "weight": 10},
            ],
        }
    )


@pytest.mark.parametrize("category", list(Category))
@pytest.mark.parametrize("budget", [5_000, 25_000, 10_000_000])
def test_gemini_plan_is_always_inside_budget(category, budget, gemini_draft):
    request = RecommendationRequest(
        category=category,
        budget=budget,
        preference="Student choice",
        notes="value first",
    )
    plan = build_plan(request, gemini_draft, model="gemini-test")

    assert plan.source == "gemini"
    assert plan.total + plan.remaining == plan.budget
    assert plan.total <= plan.budget
    assert plan.remaining > 0
    assert sum(item.amount for item in plan.items) == plan.total
    assert all(item.amount >= 100 for item in plan.items)


def test_plan_keeps_ten_percent_reserve(gemini_draft):
    request = RecommendationRequest(category="home", budget=50_000, preference="Modern")
    plan = build_plan(request, gemini_draft)
    assert plan.total == 45_000
    assert plan.remaining == 5_000


def test_larger_weight_receives_larger_amount(gemini_draft):
    request = RecommendationRequest(category="party", budget=30_000, preference="Birthday")
    plan = build_plan(request, gemini_draft)
    assert plan.items[0].amount > plan.items[1].amount > plan.items[3].amount


def test_notes_and_preference_are_cleaned():
    request = RecommendationRequest(
        category="party",
        budget=20_000,
        preference="  College   Event  ",
        notes="  30   guests   and blue theme  ",
    )
    assert request.preference == "College Event"
    assert request.notes == "30 guests and blue theme"


@pytest.mark.parametrize("budget", [0, 4_999, 10_000_001])
def test_budget_validation_rejects_out_of_range_values(budget):
    with pytest.raises(ValidationError):
        RecommendationRequest(category="home", budget=budget, preference="Modern")
