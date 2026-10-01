# API and Testing Guide

## Start the server

```bash
python -m uvicorn app.main:app --reload
```

## Swagger testing

Open `http://127.0.0.1:8000/docs`, select `POST /api/recommendations`, choose **Try it out**, paste the request below and press **Execute**.

```json
{
  "category": "party",
  "budget": 30000,
  "preference": "College Event",
  "notes": "100 guests and strong photo coverage"
}
```

Expected checks:

- HTTP status is `200`.
- `source` is `gemini`.
- `total` is not greater than `budget`.
- `total + remaining` equals `budget`.
- `items` contains practical recommendations.

## Command-line API test

```bash
curl -X POST http://127.0.0.1:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"category":"home","budget":50000,"preference":"Modern","notes":"living room first"}'
```

## Automated tests

```bash
pytest -v
pytest --cov=app --cov-report=term-missing
```

The test suite covers:

- Budget allocation for every category and boundary budget.
- Budget safety invariant.
- Notes normalization.
- Valid Gemini structured JSON.
- Gemini success, invalid-output and error paths.
- Home page and frontend serving.
- Health and category endpoints.
- Valid and invalid API requests.

## Common issues

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements-dev.txt`. |
| API returns 503 | Add a valid `GEMINI_API_KEY` to `.env`, then restart the server. |
| API returns 502 | Check internet access/API quota and try again; the app never creates a demo result. |
| Port 8000 already in use | Run `uvicorn app.main:app --reload --port 8001`. |
| API returns 422 | Use `home`, `party` or `jewellery`, a non-empty preference and a budget from 5,000 to 10,000,000. |
| GitHub Pages shows only static content | Deploy the repository to a Python/Docker hosting service. |
