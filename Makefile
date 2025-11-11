.PHONY: run api streamlit fmt lint test migrate upgrade seed

run: ## run all via docker-compose
\tdocker-compose up --build

api:
\tuvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload

streamlit:
\tstreamlit run app/Home.py --server.port 8501

fmt:
\tblack backend app scripts tests

lint:
\truff check .

test:
\tpytest -q

migrate:
\talembic -c backend/db/migrations/alembic.ini revision --autogenerate -m "auto"

upgrade:
\talembic -c backend/db/migrations/alembic.ini upgrade head

seed:
\tpython scripts/seed_demo.py
