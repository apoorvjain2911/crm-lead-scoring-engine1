from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from app.ml.predict import predict_lead

router = APIRouter()

REQUIRED_COLUMNS = [
    "company_size",
    "industry",
    "email_opens",
    "website_visits",
    "demo_requested",
    "lead_source"
]


@router.post("/bulk-predict")
async def bulk_predict(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # ---------------------------
        # VALIDATE COLUMNS
        # ---------------------------
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {missing_cols}"
            )

        results = []
        saved_leads = 0
        duplicate_leads = 0

        # ---------------------------
        # PROCESS EACH LEAD
        # ---------------------------
        for _, row in df.iterrows():
            data = row.to_dict()

            # clean NaN values (IMPORTANT)
            data = {k: (0 if pd.isna(v) else v) for k, v in data.items()}

            result = predict_lead(data)
            results.append(result)

            if result.get("duplicate"):
                duplicate_leads += 1
            elif result.get("saved"):
                saved_leads += 1

        return {
            "status": "success",
            "total_leads": len(results),
            "saved_leads": saved_leads,
            "duplicate_leads": duplicate_leads,
            "results": results
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))