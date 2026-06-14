# MLOps & Data Drift Monitoring Engine

A production-grade ML system that serves predictions via REST API
and monitors incoming data for statistical drift.

## Stack
- FastAPI + Pydantic
- scikit-learn + joblib  
- SQLAlchemy + SQLite → PostgreSQL
- Celery + Redis
- Docker Compose
- Streamlit

## Setup
pip install -r requirements.txt
python train.py
uvicorn app.main:app --reload

## Progress
- [x] Sprint 1 — Predictive API
- [x] Sprint 2 — Request logging
- [x] Sprint 3 — Drift detection
- [ ] Sprint 4 — Alert engine
- [ ] Sprint 5 — Dockerization
- [ ] Sprint 6 — Dashboard & deployment