from backend.db.session import SessionLocal
from backend.db import models
import json, os

def main():
    db = SessionLocal()
    # seed users
    path = "data/demo/demo_user_profiles.json"
    if os.path.exists(path):
        users = json.load(open(path))
        for u in users:
            if not db.query(models.User).filter(models.User.email==u["email"]).first():
                db.add(models.User(email=u["email"], name=u["name"]))
        db.commit()
    # sample run
    if not db.query(models.FootprintRun).first():
        db.add(models.FootprintRun(
            electricity_kwh=180, car_km=200, bus_km=120, diet="mixed",
            total_kg=380, energy_kg=150, travel_kg=80, food_kg=150, score=72
        ))
        db.commit()
    db.close()
    print("Seed complete.")

if __name__ == "__main__":
    main()
