"""Deterministic rupee allocation for validated Gemini recommendations."""

from __future__ import annotations

from datetime import datetime, timezone
from math import floor
from uuid import uuid4

from app.models import (
    BudgetItem,
    Category,
    GeminiDraft,
    RecommendationRequest,
    RecommendationResponse,
)


CATEGORY_META = {
    Category.HOME: {
        "title": "Home Interior",
        "description": "Furniture, lighting, décor and practical storage.",
        "icons": ["🛋️", "🪵", "💡", "🖼️", "🪴", "🧺", "🪑", "✨"],
    },
    Category.PARTY: {
        "title": "Party Planner",
        "description": "Venue, food, decoration and event essentials.",
        "icons": ["🏛️", "🍽️", "🎈", "📸", "🔊", "🎁", "🎂", "✨"],
    },
    Category.JEWELLERY: {
        "title": "Jewellery",
        "description": "A balanced purchase plan with quality and storage checks.",
        "icons": ["💎", "✨", "🪙", "📦", "🧾", "💍", "🔒", "⭐"],
    },
}


def _allocate_units(total_rupees: int, weights: list[float]) -> list[int]:
    """Allocate a ₹100-aligned target using a largest-remainder method."""
    units = total_rupees // 100
    safe_weights = [max(float(weight), 0.01) for weight in weights]
    weight_total = sum(safe_weights)
    exact = [(units * weight) / weight_total for weight in safe_weights]
    allocated = [floor(value) for value in exact]

    # Keep every displayed recommendation meaningful where the target permits it.
    if units >= len(allocated):
        allocated = [max(value, 1) for value in allocated]

    difference = units - sum(allocated)
    if difference > 0:
        order = sorted(range(len(exact)), key=lambda index: exact[index] - floor(exact[index]), reverse=True)
        for offset in range(difference):
            allocated[order[offset % len(order)]] += 1
    elif difference < 0:
        order = sorted(range(len(allocated)), key=lambda index: allocated[index], reverse=True)
        while difference < 0:
            changed = False
            for index in order:
                if allocated[index] > 1:
                    allocated[index] -= 1
                    difference += 1
                    changed = True
                    if difference == 0:
                        break
            if not changed:
                break

    return [value * 100 for value in allocated]


def build_plan(
    request: RecommendationRequest,
    draft: GeminiDraft,
    *,
    model: str | None = None,
) -> RecommendationResponse:
    meta = CATEGORY_META[request.category]
    spend_ratio = 0.90
    target = round((request.budget * spend_ratio) / 100) * 100
    target = min(request.budget, max(0, target))

    amounts = _allocate_units(target, [item.weight for item in draft.items])
    icons = meta["icons"]
    items = [
        BudgetItem(
            icon=(item.icon or icons[index % len(icons)])[:8],
            name=item.name,
            reason=item.reason,
            amount=amounts[index],
        )
        for index, item in enumerate(draft.items)
    ]
    total = sum(item.amount for item in items)

    return RecommendationResponse(
        plan_id=str(uuid4()),
        category=request.category,
        title=meta["title"],
        preference=request.preference,
        budget=request.budget,
        notes=request.notes,
        summary=draft.summary,
        items=items,
        total=total,
        remaining=request.budget - total,
        source="gemini",
        model=model,
        generated_at=datetime.now(timezone.utc),
    )
