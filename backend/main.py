from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.routes_users import router as users_router
from backend.api.routes_footprint import router as footprint_router
from backend.api.routes_reco import router as reco_router
from backend.api.routes_leaderboard import router as leaderboard_router
from backend.api.routes_reco import router as reco_router
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
app = FastAPI(title="CarbonLens API", version="0.1.0")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reco_router, prefix=settings.API_PREFIX)
app.include_router(leaderboard_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix="/api")
app.include_router(footprint_router, prefix="/api")
app.include_router(reco_router, prefix="/api")
app.include_router(leaderboard_router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": settings.DEMO_MODE}
