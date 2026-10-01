# PocketSmart AI · Tharun — Gemini + FastAPI

This repository is the complete GitHub-ready version of **PocketSmart AI · Tharun**. It keeps the same responsive dark green/lime interface as the published design and connects it to a secure FastAPI backend powered by Gemini.

Live design reference: <https://pocketsmart-ai-tharun.aswinmass2044.chatgpt.site>

## Included

- Home Interior, Party Planner and Jewellery planning flows
- Budget range from ₹5,000 to ₹1,00,00,000
- Gemini 3.8 Flash structured recommendations
- Server-side rupee allocation with a protected 10% reserve
- Saved plans in browser local storage
- FastAPI, Swagger and ReDoc
- Pydantic request/response validation
- Automated API, Gemini-service and budget-engine tests
- GitHub Actions test workflow
- Docker and Render deployment files
- Tamil setup guide, API guide, Epic map, checklist and viva answers
- No login/create-account flow
- No demo or automatic fallback recommendations

## How it works

```text
Browser form
    │ POST /api/recommendations
    ▼
FastAPI + Pydantic validation
    │
    ▼
Gemini structured JSON draft
    │
    ▼
Python budget allocator (90% plan + 10% reserve)
    │
    ▼
Validated plan displayed and optionally saved on the device
```

If the key, network or Gemini service is unavailable, the API returns a clear error. It does **not** create a demo plan.

## Project structure

```text
PocketSmart-AI-Tharun-GitHub-Complete/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   ├── budget_engine.py
│   │   └── gemini_service.py
│   └── static/
│       └── index.html
├── tests/
├── docs/
├── .github/workflows/tests.yml
├── .env.example
├── index.html
├── Dockerfile
├── render.yaml
├── requirements.txt
├── requirements-dev.txt
└── START_HERE_TAMIL.md
```

`app/static/index.html` is the frontend served by FastAPI. The root `index.html` is a matching copy for easy GitHub/phone inspection.

## Run on Windows

Python 3.10 or newer is required; Python 3.12 is recommended.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
copy .env.example .env
```

Open `.env` and add your own Gemini API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Start the project:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- Website: <http://127.0.0.1:8000>
- Swagger: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/api/health>

On macOS/Linux, activate the environment with `source .venv/bin/activate` and copy the environment file with `cp .env.example .env`.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Backend and Gemini configuration status |
| `GET` | `/api/categories` | Supported categories |
| `POST` | `/api/recommendations` | Generate a Gemini budget plan |
| `GET` | `/docs` | Interactive API testing |

Example request:

```json
{
  "category": "party",
  "budget": 30000,
  "preference": "College Event",
  "notes": "100 guests and strong photo coverage"
}
```

Supported categories are `home`, `party` and `jewellery`. The budget must be between `5000` and `10000000`.

## Run tests

Tests use a fake Gemini client, so they do not need a real key and do not consume API quota.

```bash
pytest -v
pytest --cov=app --cov-report=term-missing
```

GitHub Actions runs the same tests automatically after every push.

## Upload to GitHub

1. Extract the ZIP.
2. Create a new empty GitHub repository.
3. Upload the **files and folders inside the extracted folder**, not the ZIP itself.
4. Confirm that `app`, `tests`, `docs`, `.github`, `README.md` and `requirements.txt` are visible.
5. Never upload `.env` or a real API key. Upload `.env.example` only.

## Deploy on Render

The included `render.yaml` can create the FastAPI web service. In Render, add `GEMINI_API_KEY` as a secret environment variable. The start command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

GitHub Pages alone cannot run Python/FastAPI. For a separate static frontend, deploy the backend first and place its URL in the `pocketsmart-api-base` meta tag in the root `index.html`; also add the frontend origin to `ALLOWED_ORIGINS`.

## Security

- Keep `GEMINI_API_KEY` only in `.env` locally or the hosting secret settings.
- `.gitignore` blocks `.env` files.
- The browser never receives the Gemini key.
- API errors do not reveal secret values or internal exception details.

## Submission help

- [Tamil start guide](START_HERE_TAMIL.md)
- [API testing](docs/API_TESTING.md)
- [Epic mapping](docs/EPIC_MAPPING.md)
- [SkillWallet checklist](docs/SKILLWALLET_SUBMISSION_CHECKLIST.md)
- [Viva questions](docs/VIVA_QUESTIONS.md)
- [Verification results](docs/VERIFICATION_RESULTS.md)

## Author

Tharun — Student Project
