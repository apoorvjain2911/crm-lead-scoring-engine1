import os
import joblib
import pandas as pd

from app.db.database import SessionLocal
from app.db.models import Lead

# -----------------------------
# MODEL LOADING (SAFE PATH)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "lead_scoring_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)


def find_duplicate_lead(db, input_data):
    return (
        db.query(Lead)
        .filter(
            Lead.company_size == input_data["company_size"],
            Lead.industry == input_data["industry"],
            Lead.email_opens == input_data["email_opens"],
            Lead.website_visits == input_data["website_visits"],
            Lead.demo_requested == input_data["demo_requested"],
            Lead.lead_source == input_data["lead_source"],
        )
        .first()
    )


# -----------------------------
# SAVE TO DATABASE
# -----------------------------
def save_lead_to_db(input_data, prediction):
    db = SessionLocal()
    try:
        existing_lead = find_duplicate_lead(db, input_data)

        if existing_lead:
            return {
                "saved": False,
                "duplicate": True,
                "lead_id": existing_lead.id,
            }

        lead = Lead(
            company_size=input_data["company_size"],
            industry=input_data["industry"],
            email_opens=input_data["email_opens"],
            website_visits=input_data["website_visits"],
            demo_requested=input_data["demo_requested"],
            lead_source=input_data["lead_source"],
            probability=float(prediction["probability"]),
            score=int(prediction["score"]),
            category=prediction["category"]
        )

        db.add(lead)
        db.commit()

        db.refresh(lead)

        return {
            "saved": True,
            "duplicate": False,
            "lead_id": lead.id,
        }

    except Exception as e:
        db.rollback()
        print("DB Error:", e)
        return {
            "saved": False,
            "duplicate": False,
            "error": str(e),
        }

    finally:
        db.close()


# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_lead(data: dict):
    df = pd.DataFrame([data])

    prob = model.predict_proba(df)[0][1]
    score = int(prob * 100)

    if score >= 80:
        category = "Hot"
    elif score >= 50:
        category = "Warm"
    else:
        category = "Cold"

    result = {
        "probability": float(prob),
        "score": score,
        "category": category
    }

    # IMPORTANT: Save to DB here (so every prediction is stored)
    save_result = save_lead_to_db(data, result)
    result.update(save_result)

    return result