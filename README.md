# CarbonLens — Personal CO₂ Tracker & Climate Coach

## Stack
- Frontend: Streamlit (app/)
- Backend: FastAPI (backend/) + SQLAlchemy + PostgreSQL
- AI: Rule-based tips + basic ML profile classifier (optional)
- Config: YAML (config/)
- Orchestration: Docker Compose

## Quick Start
1) Copy env:
   cp .env.example .env
2) Start:
   docker-compose up --build
3) Open:
   - Streamlit: http://localhost:8501
   - API docs: http://localhost:8080/docs

## Dev
- Format/Lint/Tests:
  make fmt lint test

## Notes
- Emission factors live in config/emission_factors.yaml
- Demo data seeded on first run via scripts/seed_demo.py
