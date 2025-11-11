FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend
COPY config config
COPY scripts scripts
COPY data data

ENV PYTHONPATH=/app

# Alembic config path lives in backend/db/migrations/alembic.ini
RUN mkdir -p backend/db/migrations/versions

EXPOSE 8080
