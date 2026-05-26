from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import Lead

router = APIRouter()


# -------------------------
# GET ALL LEADS
# -------------------------
@router.get("/leads/all")
def get_all_leads():
    db = SessionLocal()
    try:
        leads = db.query(Lead).all()

        return {
            "total": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "company_size": l.company_size,
                    "industry": l.industry,
                    "email_opens": l.email_opens,
                    "website_visits": l.website_visits,
                    "demo_requested": l.demo_requested,
                    "lead_source": l.lead_source,
                    "probability": l.probability,
                    "score": l.score,
                    "category": l.category
                }
                for l in leads
            ]
        }
    finally:
        db.close()


# -------------------------
# HOT LEADS
# -------------------------
@router.get("/leads/hot")
def get_hot_leads():
    db = SessionLocal()
    try:
        leads = db.query(Lead).filter(Lead.score >= 80).all()

        return {
            "total": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "company_size": l.company_size,
                    "industry": l.industry,
                    "email_opens": l.email_opens,
                    "website_visits": l.website_visits,
                    "demo_requested": l.demo_requested,
                    "lead_source": l.lead_source,
                    "probability": l.probability,
                    "score": l.score,
                    "category": l.category
                }
                for l in leads
            ]
        }
    finally:
        db.close()


# -------------------------
# WARM LEADS
# -------------------------
@router.get("/leads/warm")
def get_warm_leads():
    db = SessionLocal()
    try:
        leads = db.query(Lead).filter(Lead.score >= 50, Lead.score < 80).all()

        return {
            "total": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "company_size": l.company_size,
                    "industry": l.industry,
                    "email_opens": l.email_opens,
                    "website_visits": l.website_visits,
                    "demo_requested": l.demo_requested,
                    "lead_source": l.lead_source,
                    "probability": l.probability,
                    "score": l.score,
                    "category": l.category
                }
                for l in leads
            ]
        }
    finally:
        db.close()


# -------------------------
# COLD LEADS
# -------------------------
@router.get("/leads/cold")
def get_cold_leads():
    db = SessionLocal()
    try:
        leads = db.query(Lead).filter(Lead.score < 50).all()

        return {
            "total": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "company_size": l.company_size,
                    "industry": l.industry,
                    "email_opens": l.email_opens,
                    "website_visits": l.website_visits,
                    "demo_requested": l.demo_requested,
                    "lead_source": l.lead_source,
                    "probability": l.probability,
                    "score": l.score,
                    "category": l.category
                }
                for l in leads
            ]
        }
    finally:
        db.close()


# -------------------------
# CRM STATS (STEP 7.1)
# -------------------------
@router.get("/leads/stats")
def get_lead_stats():
    db = SessionLocal()
    try:
        leads = db.query(Lead).all()

        total = len(leads)
        hot = len([l for l in leads if l.score >= 80])
        warm = len([l for l in leads if 50 <= l.score < 80])
        cold = len([l for l in leads if l.score < 50])

        avg_score = sum([l.score for l in leads]) / total if total > 0 else 0

        return {
            "total_leads": total,
            "hot_leads": hot,
            "warm_leads": warm,
            "cold_leads": cold,
            "avg_score": round(avg_score, 2),
            "hot_percentage": round((hot / total) * 100, 2) if total > 0 else 0
        }
    finally:
        db.close()