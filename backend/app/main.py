import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# existing route
from app.api.routes.predict import router as predict_router

# bulk route
from app.api.routes.bulk_predict import router as bulk_router
from app.api.routes import leads

# Create app instance
app = FastAPI(
    title="CRM Lead Scoring Engine",
    description="AI-powered lead scoring using Logistic Regression",
    version="1.0.0"
)

# Allowed frontend origins
def get_cors_origins():
    configured_origins = os.getenv("ALLOWED_ORIGINS")

    if configured_origins:
        return [
            origin.strip()
            for origin in configured_origins.split(",")
            if origin.strip()
        ]

    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://crm-lead-scoring-engine1.vercel.app",
    ]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(leads.router)
app.include_router(predict_router)
app.include_router(bulk_router)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "CRM Lead Scoring API is running"
    }

# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }