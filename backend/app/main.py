from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# existing route
from app.api.routes.predict import router as predict_router

# NEW bulk route (STEP 1.1)
from app.api.routes.bulk_predict import router as bulk_router
from app.api.routes import leads

# Create app instance
app = FastAPI(
    title="CRM Lead Scoring Engine",
    description="AI-powered lead scoring using Logistic Regression",
    version="1.0.0"
)

# CORS - allow frontend dev server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(leads.router)
app.include_router(predict_router)
app.include_router(bulk_router)


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