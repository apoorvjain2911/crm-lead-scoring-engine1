# crm-lead-scoring-engine1

AI-powered CRM Lead Scoring Engine — a minimal full-stack demo that scores leads
using a trained model and exposes a frontend dashboard to review, filter, and
bulk-upload lead data.

Features
- FastAPI backend with endpoints to predict, bulk-predict (CSV upload), and
	list leads by category (hot/warm/cold).
- Simple SQLite persistence for demo purposes (see `backend/crm_leads.db`).
- React + Vite frontend dashboard with upload, filters, stats, and table.
- Duplicate-lead detection (exact-match) on save to avoid inserting the same
	lead twice.

Quick start (local)

Prerequisites
- Python 3.10+
- Node.js 18+ and npm

Backend
1. Create and activate a virtual environment inside `backend/` and install requirements:

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1   # PowerShell on Windows
pip install -r requirements.txt
```

2. Initialize DB (optional - the repo includes a demo DB):

```powershell
python app/db/init_db.py
```

3. Run the backend API:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend
1. Install dependencies and run dev server (from repo root or `frontend/`):

```powershell
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

2. Build for production:

```powershell
npm run build
```

API endpoints (local)
- GET /leads/all — list all leads
- GET /leads/hot — leads with score >= 80
- GET /leads/warm — 50 <= score < 80
- GET /leads/cold — score < 50
- GET /leads/stats — aggregated stats (total, hot/warm/cold counts, avg score)
- POST /predict — single lead prediction (JSON body)
- POST /bulk-predict — multipart CSV upload; returns saved/duplicate counts

Notes on duplicates
- The backend now performs an exact-match check across the core input fields
	(company_size, industry, email_opens, website_visits, demo_requested,
	lead_source) and will skip saving rows that already exist. The bulk upload
	response includes `saved_leads` and `duplicate_leads` counts.

Deployment hints
- Frontend: any static host that supports Vite-built assets (Vercel, Netlify,
	GitHub Pages). Build the frontend with `npm run build` and deploy the `dist/`
	output.
- Backend: can be deployed to Render, Railway, or Heroku-like services. Ensure
	to use a persistent DB for production (the demo uses SQLite for simplicity).

Repository
- This repository includes both `backend/` and `frontend/` folders. A single
	commit was pushed with the dashboard and dedupe flow implemented.

If you want, I can add a dedicated `deploy/` guide for a specific provider
(Vercel + Render) and provide the exact steps and environment variables.

---

## Full README (detailed)

This README contains step-by-step instructions to run the project locally
and recommended deployment options.

### Repository layout

- `backend/` — FastAPI application, model code, and SQLite demo DB
- `frontend/` — React + Vite dashboard

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

### Backend — Local setup

1. Open a terminal and change into the backend folder:

```powershell
cd backend
```

2. Create and activate a Python virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1    # PowerShell
# or: venv\Scripts\activate  # cmd.exe
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. (Optional) Initialize the database tables:

```powershell
python app/db/init_db.py
```

5. Run the API locally:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

### Frontend — Local setup

1. From the repo root (or `frontend/`):

```powershell
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

2. Build for production:

```powershell
npm run build
```

The built assets will be in `frontend/dist`.

### API endpoints (summary)

- `GET /leads/all` — list all leads (JSON: `{ total, leads: [...] }`)
- `GET /leads/hot` — leads with `score >= 80`
- `GET /leads/warm` — `50 <= score < 80`
- `GET /leads/cold` — `score < 50`
- `GET /leads/stats` — aggregated stats (`total_leads`, `hot_leads`, `avg_score`, ...)
- `POST /predict` — single JSON lead -> prediction
- `POST /bulk-predict` — multipart CSV upload; returns `total_leads`, `saved_leads`, `duplicate_leads`, and per-row `results`.

CSV schema required for `bulk-predict` (columns):

```
company_size,industry,email_opens,website_visits,demo_requested,lead_source
```

### Duplicate handling

The backend performs an exact-match dedupe on the fields above before saving
predictions to the DB. Upload responses include how many rows were saved vs
skipped as duplicates.

### Deployment recommendations

Frontend (recommended): Vercel, Netlify, or any static hosting.

- Build with `npm run build` and deploy `frontend/dist`.
- If using Vercel, connect the repo and set the project to build `frontend`
	and output the `dist` folder. No backend config required on Vercel for
	the static site.

Backend (recommended): Render, Railway, or a VPS/container host.

- Use a production DB (Postgres) instead of the included SQLite DB.
- Configure the service to run `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Expose the backend URL as an environment variable for the frontend (if
	required), or update `frontend/src/api/leads.js` BASE_URL to the deployed API.

Quick deploy notes — sample provider choices

- Vercel (frontend): connect repo, set root to `frontend`, build command `npm run build`, output folder `dist`.
- Render / Railway (backend): Create a Python web service, set start command
	to `uvicorn app.main:app --host 0.0.0.0 --port 8000`, set environment variables, and attach a managed Postgres instance for production.

### Security & production notes

- Do not commit model artifacts or DB files to a public repo in production.
- Use a real database, secure credentials with environment variables, and
	consider rate-limiting / auth on the API.

### Troubleshooting

- If the frontend can't reach the API in production, update `BASE_URL` in
	`frontend/src/api/leads.js` to point to the deployed backend URL.
- Check CORS: `app/main.py` enables CORS for local dev origins; adjust for
	your production domain.

---

If you'd like, I can add GitHub Actions or Render/Vercel configuration files
and a step-by-step deploy guide for your chosen provider. Tell me which
provider you'd prefer and I'll scaffold the exact deploy configuration.

