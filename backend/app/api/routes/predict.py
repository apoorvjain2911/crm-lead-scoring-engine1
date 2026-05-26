from fastapi import APIRouter
from app.ml.predict import predict_lead

from pydantic import BaseModel

router = APIRouter()


# -----------------------------
# REQUEST SCHEMA (IMPORTANT)
# -----------------------------
class LeadInput(BaseModel):
    company_size: int
    industry: str
    email_opens: int
    website_visits: int
    demo_requested: int
    lead_source: str


# -----------------------------
# SINGLE LEAD PREDICTION API
# -----------------------------
@router.post("/predict")
def predict(data: LeadInput):
    result = predict_lead(data.dict())
    return {
        "status": "success",
        "input": data,
        "prediction": result
    }