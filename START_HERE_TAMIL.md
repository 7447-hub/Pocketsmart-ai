# முதலில் இதைப் படிக்கவும் — PocketSmart AI · Tharun

Machi, இது Tharun website design மட்டும் இல்லை. இந்த package-ல் **same UI + Gemini AI + FastAPI backend + validation + tests + GitHub/Render files** எல்லாமே இருக்கு.

முக்கியமாக:

- Login / Create Account இல்லை.
- Demo mode இல்லை.
- Local sample recommendation இல்லை.
- Plan generate ஆக real Gemini key தேவை.
- API key browser code-ல் அல்லது GitHub-ல் போடக்கூடாது.

## Laptop-ல் முதல் முறை setup

1. ZIP file-ஐ extract பண்ணு.
2. Extract செய்த folder-ஐ VS Code-ல் open பண்ணு.
3. Terminal open பண்ணி இந்த commands run பண்ணு:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
copy .env.example .env
```

## Gemini API key add செய்வது

1. Google AI Studio open பண்ணு: <https://aistudio.google.com/app/apikey>
2. புதிய API key create பண்ணு.
3. Project folder-ல் `.env` file open பண்ணு.
4. இந்த line-ல் உன் key paste பண்ணு:

```env
GEMINI_API_KEY=your_real_key_here
```

`.env.example` file-ல் key paste பண்ணாதே. `.env` file-ஐ GitHub-க்கு upload பண்ணாதே.

## Website start செய்வது

```powershell
python -m uvicorn app.main:app --reload
```

Browser-ல் open பண்ண வேண்டியது:

- Website: `http://127.0.0.1:8000`
- API testing: `http://127.0.0.1:8000/docs`
- Health status: `http://127.0.0.1:8000/api/health`

`/api/health` response-ல் `gemini_configured: true` வந்தால் key correct-ஆ load ஆகியிருக்கு.

## எப்படி test பண்ணுவது

Website-ல் இந்த மூன்று sample-யும் try பண்ணு:

1. Home Interior — ₹50,000 — Modern
2. Party Planner — ₹30,000 — College Event
3. Jewellery — ₹25,000 — Daily Wear

Result-ல் `Gemini` tag, recommendations, Budget, Planned, Balance எல்லாம் வர வேண்டும்.

Automated tests:

```powershell
pytest -v
```

எல்லா tests-க்கும் `PASSED` வர வேண்டும். Test screenshot-ஐ submission proof-ஆ save பண்ணிக்கோ.

## GitHub-க்கு upload செய்வது

ZIP file-ஐ நேராக upload பண்ணாதே. ZIP extract செய்த பிறகு அதன் உள்ளே இருக்கும் files/folders அனைத்தையும் repository root-க்கு upload பண்ணு.

GitHub repository-ல் இவை கண்டிப்பாக இருக்க வேண்டும்:

- `app` folder
- `tests` folder
- `docs` folder
- `.github/workflows/tests.yml`
- `.env.example`
- `README.md`
- `requirements.txt`
- `Dockerfile`
- `render.yaml`

Upload செய்யக்கூடாதது:

- `.env`
- Real Gemini API key
- `.venv` folder
- `__pycache__` folders

## GitHub Pages மட்டும் போதுமா?

போதாது. GitHub Pages HTML/CSS/JavaScript மட்டும் run செய்யும்; Python FastAPI மற்றும் Gemini secret key run செய்யாது. Full project demo-க்கு Render போன்ற Python hosting use பண்ணு.

Render dashboard-ல் `GEMINI_API_KEY`-ஐ secret environment variable-ஆ add பண்ண வேண்டும். Source code-ல் key எழுத வேண்டாம்.

## Submission screenshots

1. Website home page
2. Gemini result with totals
3. Saved Plans screen
4. `/docs` Swagger screen
5. `pytest -v` PASSED screen
6. GitHub repository files screen
7. Hosted live link screen

Full checklist: `docs/SKILLWALLET_SUBMISSION_CHECKLIST.md`
