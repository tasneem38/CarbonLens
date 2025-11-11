from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)

class FootprintRun(Base):
    __tablename__ = "footprint_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    electricity_kwh: Mapped[float] = mapped_column(Float)
    car_km: Mapped[float] = mapped_column(Float)
    bus_km: Mapped[float] = mapped_column(Float)
    diet: Mapped[str] = mapped_column(String)
    total_kg: Mapped[float] = mapped_column(Float)
    energy_kg: Mapped[float] = mapped_column(Float)
    travel_kg: Mapped[float] = mapped_column(Float)
    food_kg: Mapped[float] = mapped_column(Float)
    score: Mapped[int] = mapped_column(Integer)

from sqlalchemy import Column, Integer, String, DateTime, func
from .session import Base

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, default="Anonymous")
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
