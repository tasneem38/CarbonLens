from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db import models

router = APIRouter(tags=["leaderboard"])

@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    rows = db.query(models.FootprintRun).order_by(models.FootprintRun.score.desc()).limit(10).all()
    return [{"name": f"User #{r.user_id or 0}", "score": r.score, "total_kg": r.total_kg} for r in rows]

from fastapi import APIRouter
from backend.db.session import SessionLocal
from backend.db.models import Leaderboard

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])
@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    """Return top scores ranked by score descending"""
    leaderboard = db.query(Leaderboard).order_by(Leaderboard.score.desc()).limit(10).all()
    return [
        {"name": entry.user_name, "score": round(entry.score, 2), "created_at": entry.created_at}
        for entry in leaderboard
    ]