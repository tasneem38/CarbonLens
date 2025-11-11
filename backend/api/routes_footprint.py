from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.schemas import LifestyleInput, FootprintResult, FootprintTotals, TrendPoint
from backend.db.session import get_db
from backend.db import models
from backend.db.models import Leaderboard
from backend.services.calculator import compute_footprint as compute_totals
from backend.services.scoring import green_score as score_from_total
from backend.services.forecasting import naive_forecast_series as build_trend

router = APIRouter(prefix="/footprint", tags=["Footprint"])

@router.post("/compute", response_model=FootprintResult)
def compute_footprint(payload: LifestyleInput, db: Session = Depends(get_db)):
    # Convert payload to dict for processing
    payload_dict = payload.model_dump()
    
    # 1️⃣ Calculate emission totals
    totals = compute_totals(payload_dict)

    # 2️⃣ Calculate Green Score
    score = score_from_total(totals["total"])

    # 3️⃣ Generate trend forecast
    trend = build_trend(totals["total"])

    # 4️⃣ Save full footprint run to database
    run = models.FootprintRun(
        user_id=None,
        inputs=payload_dict,
        total_kg=totals["total"],
        energy_kg=totals["energy"],
        travel_kg=totals["travel"],
        food_kg=totals["food"],
        goods_kg=totals.get("goods", 0),
        score=score
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # 5️⃣ Save to leaderboard table
    entry = Leaderboard(
        user_name="Guest User",
        score=score
    )
    db.add(entry)
    db.commit()

    # 6️⃣ Return response for frontend
    return FootprintResult(
        inputs=payload,
        totals=FootprintTotals(**totals),
        score=score,
        trend=[TrendPoint(**p) for p in trend],
        recommendations=[]
    )