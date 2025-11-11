from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

# ----------------- Inputs -----------------
class LifestyleInput(BaseModel):
    electricityKwh: float = 0
    naturalGasTherms: float = 0
    carKm: float = 0
    busKm: float = 0
    diet: Literal["veg", "mixed", "nonveg"] = "mixed"
    foodEmissions: float = 0
    goodsEmissions: float = 0

# ----------------- Footprint Response -----------------
class FootprintTotals(BaseModel):
    total: float
    energy: float
    travel: float
    food: float
    goods: float = 0

class TrendPoint(BaseModel):
    x: str
    y: float

class FootprintResult(BaseModel):
    inputs: LifestyleInput
    totals: FootprintTotals
    score: int
    trend: List[TrendPoint]
    recommendations: List[Dict] = []

# ----------------- AI Tips -----------------
class TipsResponse(BaseModel):
    tips: List[Dict]

# -------- Optional: Keep only if using users --------
class UserCreate(BaseModel):
    email: str

class UserOut(BaseModel):
    id: int
    email: str