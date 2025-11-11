from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)

from sqlalchemy import Column, Integer, Float, JSON, DateTime, func

class FootprintRun(Base):
    __tablename__ = "footprint_runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    inputs = Column(JSON, nullable=True)  # ✅ Add this line
    total_kg = Column(Float, nullable=False)
    energy_kg = Column(Float, nullable=False)
    travel_kg = Column(Float, nullable=False)
    food_kg = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

from sqlalchemy import Column, Integer, String, DateTime, func
from .session import Base

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, default="Anonymous")
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())