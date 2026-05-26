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

