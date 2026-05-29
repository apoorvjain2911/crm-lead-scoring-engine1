import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routes
from app.api.routes.predict import router as predict_router
from app.api.routes.bulk_predict import router as bulk_router
from app.api.routes import leads

# Create app instance
app = FastAPI(
    title="CRM Lead Scoring Engine",
    description="AI-powered lead scoring using Logistic Regression",
    version="1.0.0"
)

# -----------------------------
# CORS CONFIG (FIXED FOR PROD)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://crm-lead-scoring-engine1.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTES
# -----------------------------
app.include_router(leads.router)
app.include_router(predict_router)
app.include_router(bulk_router)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "CRM Lead Scoring API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }